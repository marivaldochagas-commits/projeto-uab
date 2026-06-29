import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(const MaterialApp(home: TesteConexao()));

class TesteConexao extends StatefulWidget {
  const TesteConexao({super.key});
  @override
  State<TesteConexao> createState() => _TesteConexaoState();
}

class _TesteConexaoState extends State<TesteConexao> {
  List chamados = [];
  String mensagemStatus = "Sistema pronto para uso";
  final String token = "SEU_TOKEN_AQUI";

  Future<void> buscarChamados() async {
    final url = Uri.parse('http://10.0.2.2:5000/api/chamados');
    try {
      final response = await http.get(url, headers: {'Authorization': 'Bearer $token'});
      if (response.statusCode == 200) {
        setState(() {
          chamados = jsonDecode(response.body);
          mensagemStatus = "Chamados carregados com sucesso!";
        });
      }
    } catch (e) {
      setState(() => mensagemStatus = "Erro de conexão: $e");
    }
  }

  Future<void> criarChamado() async {
    final url = Uri.parse('http://10.0.2.2:5000/api/chamados');
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer $token'},
        body: jsonEncode({"descricao": "Chamado via App", "status": "Aberto", "cliente_id": 1, "titulo": "App"}),
      );
      if (response.statusCode == 201 || response.statusCode == 200) {
        setState(() => mensagemStatus = "Chamado criado!");
        buscarChamados();
      }
    } catch (e) {
      setState(() => mensagemStatus = "Erro ao criar");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.blueAccent,
        title: Row(
          children: [
            Image.asset(
              'assets/logo_holding.png',
              height: 30,
              errorBuilder: (context, error, stackTrace) => const Icon(Icons.business, color: Colors.white),
            ),
            const SizedBox(width: 10),
            const Text("Zil Atendimento", style: TextStyle(color: Colors.white)),
          ],
        ),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Text(mensagemStatus),
          ),
          Expanded(
            child: ListView.separated(
              itemCount: chamados.length,
              separatorBuilder: (ctx, i) => const Divider(),
              itemBuilder: (context, index) {
                return ListTile(
                  title: Text(chamados[index]['descricao'] ?? 'Sem descrição'),
                  subtitle: Text('Status: ${chamados[index]['status'] ?? 'N/A'}'),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(20.0),
            child: Row(
              children: [
                Expanded(
                    child: ElevatedButton.icon(
                        onPressed: buscarChamados,
                        icon: const Icon(Icons.refresh),
                        label: const Text("Buscar"))),
                const SizedBox(width: 15),
                Expanded(
                    child: ElevatedButton.icon(
                        onPressed: criarChamado,
                        icon: const Icon(Icons.add),
                        label: const Text("Novo"),
                        style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.green,
                            foregroundColor: Colors.white))),
              ],
            ),
          ),
        ],
      ),
    );
  }
}