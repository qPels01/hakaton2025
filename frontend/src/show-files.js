// src/show-files.js

import fs from 'fs';
import path from 'path';

const IGNORE_DIRS = ['node_modules', '.git'];

function isTargetFile(filename) {
    return (
        (filename.endsWith('.ts') ||
         filename.endsWith('.js') ||
         filename.endsWith('.vue') ||
         filename.endsWith('.env')) &&
        !filename.includes("show-files")
    );
}

function collectFiles(dir, output) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });

    for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);

        if (entry.isDirectory()) {
            if (!IGNORE_DIRS.includes(entry.name)) {
                collectFiles(fullPath, output);
            }
        } else if (entry.isFile() && isTargetFile(entry.name)) {
            output.push(`\n==== Файл: ${fullPath} ====\n`);
            const content = fs.readFileSync(fullPath, 'utf-8');
            output.push(content);
        }
    }
}

// чтобы получить __dirname в ESM:
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const targetDir = process.argv[2]
    ? path.resolve(process.argv[2])
    : path.resolve(__dirname, '..');

const outputFile = 'files-output.txt';

if (!fs.existsSync(targetDir) || !fs.statSync(targetDir).isDirectory()) {
    console.error('Путь не найден или не является директорией:', targetDir);
    process.exit(1);
}

const result = [];
collectFiles(targetDir, result);

fs.writeFileSync(outputFile, result.join('\n'), 'utf-8');
console.log(`Операция завершена. Результат сохранён в "${outputFile}"`);