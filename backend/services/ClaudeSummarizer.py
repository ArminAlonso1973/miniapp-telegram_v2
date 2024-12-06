import os
import re
import asyncio
from typing import List, Dict
from dotenv import load_dotenv
import anthropic
import PyPDF2
from quart import Quart, request, jsonify

class ClaudeSummarizer:
    def __init__(self, chunk_size: int = 1024, batch_size: int = 4):
        load_dotenv()
        self.client = anthropic.Anthropic(
            api_key=os.getenv('ANTHROPIC_API_KEY')
        )
        self.chunk_size = chunk_size
        self.batch_size = batch_size

    async def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extracción asincrónica de texto de PDF"""
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text

    def preprocess_text(self, text: str) -> str:
        """Preprocesamiento de texto"""
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,!?]', '', text)
        return text.strip()

    def create_chunks(self, text: str) -> List[str]:
        """División de texto en chunks"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1
            if current_length + word_length > self.chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = word_length
            else:
                current_chunk.append(word)
                current_length += word_length
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

    async def summarize_chunk(self, chunk: str) -> str:
        """Resumen asincrónico de un chunk"""
        try:
            # Usar run_in_executor para hacer la llamada a la API de manera asincrónica
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=300,
                    messages=[
                        {
                            "role": "user",
                            "content": f"Resume el siguiente texto capturando los puntos principales de manera concisa:\n\n{chunk}"
                        }
                    ]
                )
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error al resumir chunk: {e}")
            return ""

    async def summarize_document(self, pdf_path: str) -> Dict[str, str]:
        """Resumen asincrónico de documento completo"""
        # Extracción de texto
        text = await self.extract_text_from_pdf(pdf_path)
        clean_text = self.preprocess_text(text)
        chunks = self.create_chunks(clean_text)
        
        # Procesamiento asincrónico de chunks
        summaries = []
        for i in range(0, len(chunks), self.batch_size):
            batch = chunks[i:i + self.batch_size]
            # Usar gather para procesar chunks en paralelo
            batch_summaries = await asyncio.gather(
                *[self.summarize_chunk(chunk) for chunk in batch]
            )
            summaries.extend(batch_summaries)
        
        # Generar resumen final
        final_summary = " ".join(summaries)
        
        return {
            "original_length": len(clean_text),
            "summary_length": len(final_summary),
            "summary": final_summary
        }

# Aplicación Quart
app = Quart(__name__)
summarizer = ClaudeSummarizer()

@app.route('/summarize', methods=['POST'])
async def summarize():
    try:
        # Recibir archivo PDF
        form = await request.form
        files = await request.files
        pdf_file = files.get('pdf')
        
        if not pdf_file:
            return jsonify({"error": "No se proporcionó archivo PDF"}), 400
        
        # Guardar archivo temporalmente
        pdf_path = f"temp_{pdf_file.filename}"
        await pdf_file.save(pdf_path)
        
        try:
            # Generar resumen asincrónico
            resultado = await summarizer.summarize_document(pdf_path)
            return jsonify(resultado)
        finally:
            # Eliminar archivo temporal
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Configuración para ejecución
if __name__ == '__main__':
    app.run(debug=True)