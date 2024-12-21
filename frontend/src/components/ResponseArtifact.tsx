import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

interface Response {
  content: string;
  references?: string[];
}

const ResponseArtifact: React.FC<{ response: Response }> = ({ response }) => (
  <Card className="bg-gray-700 border-gray-600">
    <CardHeader className="pb-2">
      <CardTitle className="text-sm text-gray-300">Respuesta del Asistente</CardTitle>
    </CardHeader>
    <CardContent>
      <p className="text-gray-200 mb-4">{response.content}</p>
      {response.references && (
        <div className="border-t border-gray-600 pt-2">
          <p className="text-sm text-gray-400">Referencias:</p>
          <ul className="text-sm text-yellow-500">
            {response.references.map((ref: string, idx: number) => (
              <li key={idx}>{ref}</li>
            ))}
          </ul>
        </div>
      )}
    </CardContent>
  </Card>
);

export default ResponseArtifact;
