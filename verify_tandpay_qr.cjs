const path = require('node:path');
const sharp = require('sharp');
const jsQR = require('jsqr');

async function decode(filename, extract) {
  let image = sharp(filename);
  if (extract) image = image.extract(extract);
  const { data, info } = await image.ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  const code = jsQR(new Uint8ClampedArray(data), info.width, info.height, { inversionAttempts: 'dontInvert' });
  if (!code || code.data !== 'https://tandpay.com') {
    throw new Error(`QR verification failed for ${filename}; decoded ${code?.data ?? 'nothing'}`);
  }
  console.log(`QR VERIFIED: ${path.basename(filename)} => ${code.data}`);
}

async function main() {
  await decode(path.join(__dirname, 'assets/tandpay-com-qr.png'));
  await decode(path.join(__dirname, 'v3/tandpay-escrow-booth-preview.png'));
  await decode(path.join(__dirname, 'v3/tandpay-escrow-booth-8000px.png'), {
    left: 1550 * 4,
    top: 375 * 4,
    width: 320 * 4,
    height: 320 * 4,
  });
}

main().catch(error => { console.error(error); process.exit(1); });
