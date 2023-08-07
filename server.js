const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000; // Pode ser qualquer porta disponível

// Middleware para analisar o corpo das requisições (parse do JSON)
app.use(bodyParser.json());

// Rota para autenticação do usuário (simulação)
app.post('/api/login', (req, res) => {
    const { email, password } = req.body;
    // Simulação de autenticação bem-sucedida
    if (email === 'user@example.com' && password === 'senha123') {
        res.status(200).json({ success: true, message: 'Login realizado com sucesso!' });
    } else {
        res.status(401).json({ success: false, message: 'E-mail ou senha incorretos.' });
    }
});

app.listen(port, () => {
    console.log(`Servidor backend rodando em http://localhost:${port}`);

});