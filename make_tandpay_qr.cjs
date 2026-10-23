const fs = require('node:fs');
const path = require('node:path');
const QRCode = require('qrcode');

async function main() {
  const destination = 'https://tandpay.com';
  const options = {
    errorCorrectionLevel: 'Q',
    margin: 4,
    color: { dark: '#000000', light: '#FFFFFF' },
  };
  const assets = path.join(__dirname, 'assets');
  const code = QRCode.create(destination, options);
  const svg = await QRCode.toString(destination, { ...options, type: 'svg' });
  fs.writeFileSync(path.join(assets, 'tandpay-com-qr.svg'), svg);
  await QRCode.toFile(path.join(assets, 'tandpay-com-qr.png'), destination, {
    ...options,
    type: 'png',
    scale: 20,
  });
  const metadata = {
    destination,
    errorCorrectionLevel: 'Q',
    quietZoneModules: 4,
    symbolModules: code.modules.size,
    generator: 'qrcode',
    generatorVersion: require('qrcode/package.json').version,
    trackingOrRedirectService: false,
  };
  fs.writeFileSync(path.join(assets, 'tandpay-com-qr.json'), JSON.stringify(metadata, null, 2) + '\n');
  console.log('Generated QR:', JSON.stringify(metadata));
}

main().catch(error => { console.error(error); process.exit(1); });
