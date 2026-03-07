const express = require('express');
const http = require('http');
const { WebSocketServer } = require('ws');
const { exec } = require('child_process');

const port = 3001;

// HTTP Server
const app = express();
const server = http.createServer(app);

// WebSocket Server
const wss = new WebSocketServer({ server });

wss.on('connection', (ws) => {
  console.log('Klient ulandi.');

  ws.on('message', (message) => {
    const command = message.toString();
    console.log(`Qabul qilingan buyruq: ${command}`);

    // Yechim: Buyruqlarni boshqarish
    handleCommand(command, ws);
  });

  ws.on('close', () => {
    console.log('Klient uzildi.');
  });

  ws.send('Jarvis backend-ga muvaffaqiyatli ulandingiz!');
});

/**
 * Buyruqlarni qayta ishlash va bajarish.
 * @param {string} command - Foydalanuvchidan kelgan buyruq.
 * @param {WebSocket} ws - Mijoz bilan WebSocket aloqasi.
 */
function handleCommand(command, ws) {
  const lowerCaseCommand = command.toLowerCase();

  // Oddiy buyruqlar uchun misollar
  if (lowerCaseCommand.includes('och')) {
    // Masalan: "brauzerni och" yoki "och fayl menedjerini"
    let appToOpen = '';
    if (lowerCaseCommand.includes('brauzer')) {
        appToOpen = 'xdg-open http://google.com'; // Linux uchun
    } else if (lowerCaseCommand.includes('fayl menedjeri')) {
        appToOpen = 'xdg-open .'; // Linux uchun joriy papkani ochish
    } else if (lowerCaseCommand.includes('chatgpt')) {
        appToOpen = 'xdg-open https://chat.openai.com';
    } else if (lowerCaseCommand.includes('uzmovi')) {
        appToOpen = 'xdg-open https://uzmovi.com';
    }
    // ... boshqa dasturlar uchun shartlar qo'shishingiz mumkin

    if (appToOpen) {
      exec(appToOpen, (error, stdout, stderr) => {
        if (error) {
          const errorMessage = `Xatolik: ${error.message}`;
          console.error(errorMessage);
          ws.send(`Buyruqni bajarishda xatolik: ${appToOpen}`);
          return;
        }
        const successMessage = `"${appToOpen}" buyrug'i muvaffaqiyatli bajarildi.`;
        console.log(successMessage);
        ws.send(successMessage);
      });
    } else {
        ws.send(`"${command}" buyrug'i uchun mos dastur topilmadi.`);
    }
  } else if (lowerCaseCommand.startsWith('qaytar ')) {
      const textToRepeat = command.substring(7);
      ws.send(`Siz aytdingiz: ${textToRepeat}`);
  }
  
  // TODO: AI modeliga ulanish va murakkab so'rovlarni qayta ishlash
  // else {
  //   ws.send(`Noma'lum buyruq: ${command}`);
  // }
}

server.listen(port, () => {
  console.log(`Server ${port}-portda ishga tushdi.`);
});
