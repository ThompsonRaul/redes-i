import net from "net";

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.status(405).json({ error: "Method not allowed" });
    return;
  }

  const { command } = req.body;

  // Verifica se há um comando
  if (!command) {
    res.status(400).json({ error: "No command provided" });
    return;
  }

  const client = new net.Socket();

  // Conecta ao servidor de notas
  client.connect(9998, "127.0.0.1", () => {
    client.write(command); // Envia o comando ao servidor de notas
  });

  // Quando o servidor responde, envia a resposta de volta ao cliente da API
  client.on("data", (data) => {
    res.status(200).json({ response: data.toString() });
    client.end(); // Fecha o cliente após obter a resposta
  });

  // Trata erros de conexão ao servidor de notas
  client.on("error", (error) => {
    console.error("TCP socket error:", error);
    res.status(500).json({ error: "Error connecting to the notes server." });
    client.end();
  });

  client.on("close", () => {
    console.log("TCP connection closed.");
  });
}
