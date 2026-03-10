// 运行指令为  node src/utils/compress.js 在根目录下运行
import sharp from 'sharp';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 配置输入和输出目录
const inputDir = path.join(__dirname, '../../public/imgs/openComputer');
const outputDir = path.join(__dirname, '../../public/imgs/openComputer_compressed');

// 如果输出目录不存在，就创建它
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// 遍历输入目录下的所有文件
fs.readdirSync(inputDir).forEach((file) => {
  const ext = path.extname(file).toLowerCase();
  // 只处理 PNG/JPG/JPEG 图片
  if (ext === '.png' || ext === '.jpg' || ext === '.jpeg') {
    sharp(path.join(inputDir, file))
      .png({ quality: 80 }) // 保持PNG格式，质量80（可调整）
      .toFile(path.join(outputDir, file))
      .then(() => console.log(`压缩完成: ${file}`))
      .catch((err) => console.error(`处理失败: ${file}`, err));
  }
});
