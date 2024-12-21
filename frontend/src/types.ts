export interface Chat {
  question: string;
  answer: {
    content: string;
    references?: string[]; // Permite que `references` sea opcional
  };
}
