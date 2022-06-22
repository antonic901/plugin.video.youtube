const { app, BrowserWindow } = require("electron");

// closes windows that keeps poping up when installing app on windows
if (require('electron-squirrel-startup')) return app.quit();

const server = require("./backend/bin");

let window;

function createWindow() {
  window = new BrowserWindow({
    width: 1280,
    height: 720,
    // icon: path.join(app.getAppPath(), './assets/icon.png'),
    webPreferences: {
      nodeIntegration: true,
    },
  });

  window.loadURL('http://' + server.host + ':' + server.port);
  window.on("closed", function () {
    window = null;
  });
}

app.whenReady().then(() => {
  createWindow()

  // Use this if app is for macOS
  // app.on('activate', () => {
  //   if (BrowserWindow.getAllWindows().length === 0) createWindow()
  // })

})

app.on("resize", (e, x, y) => {
  window.setSize(x, y);
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

// Use this if app is for WIN/Linux
app.on("activate", () => {
  if (window === null) {
    createWindow();
  }
});
