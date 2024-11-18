import { useState } from "react";

export default function Home() {
  const [command, setCommand] = useState("");
  const [response, setResponse] = useState("");

  const handleSendCommand = async () => {
    try {
      const res = await fetch("/api/notes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command }),
      });

      const data = await res.json();
      setResponse(data.response || data.error);
    } catch (error) {
      console.error("Error sending command:", error);
      setResponse("Error sending command to the server.");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Gerenciador de Notas</h1>
      <input
        type="text"
        value={command}
        onChange={(e) => setCommand(e.target.value)}
        placeholder="Digite o comando (ex., CREATE_NOTE Olá mundo!)"
        style={{ width: "320px", marginRight: "10px" }}
      />
      <button onClick={handleSendCommand}>Enviar Comando</button>
      <div style={{ marginTop: "20px" }}>
        <h2>Resposta</h2>
        <p>{response}</p>
      </div>
    </div>
  );
}
