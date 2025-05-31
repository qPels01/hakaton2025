import fs from 'fs';
import path from 'path';

// Папки, которые надо игнорировать
const IGNORE_DIRS = ['node_modules', '.git'];

// Проверка по расширению
function isTargetFile(filename: string): boolean {
    return filename.endsWith('.ts') || filename.endsWith('.env');
}

// Собирает данные по найденным файлам
function collectFiles(dir: string, output: string[]): void {
    const entries = fs.readdirSync(dir, { withFileTypes: true });

    for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);

        if (entry.isDirectory()) {
            if (!IGNORE_DIRS.includes(entry.name)) {
                collectFiles(fullPath, output); // Рекурсия
            }
        } else if (entry.isFile() && isTargetFile(entry.name)) {
            output.push(`\n==== Файл: ${fullPath} ====\n`);
            const content = fs.readFileSync(fullPath, 'utf-8');
            output.push(content);
        }
    }
}

// Если путь передан в аргументах — используем его, иначе ../ (вышестоящая директория)
const targetDir = process.argv[2]
    ? path.resolve(process.argv[2])
    : path.resolve(process.cwd(), '..');
// Имя выходного файла
const outputFile = 'files-output.txt';

if (!fs.existsSync(targetDir) || !fs.statSync(targetDir).isDirectory()) {
    console.error('Путь не найден или не является директорией:', targetDir);
    process.exit(1);
}

const result: string[] = [];
collectFiles(targetDir, result);

// Сохраняем в файл
fs.writeFileSync(outputFile, result.join('\n'), 'utf-8');
console.log(`Операция завершена. Результат сохранён в "${outputFile}"`);