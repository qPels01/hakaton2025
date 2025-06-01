import * as fs from 'fs';
import * as path from 'path';

// Укажите директории, которые нужно игнорировать при обходе
const IGNORE_DIRS = ['node_modules', '.git', 'dist'];
// Укажите имя этого скрипта, чтобы не обрабатывать себя
const THIS_SCRIPT = path.basename(__filename);

function isTargetFile(filename: string): boolean {
    return (
        (filename.endsWith('.ts') || filename.endsWith('.env') || filename.endsWith('developers.json')) &&
        filename !== THIS_SCRIPT
    );
}

function collectFiles(dir: string, output: string[]): void {
    // Получаем список файлов и папок внутри директории
    const entries = fs.readdirSync(dir, { withFileTypes: true });

    for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);

        // Если это директория, рекурсивно обрабатываем её
        if (entry.isDirectory()) {
            if (!IGNORE_DIRS.includes(entry.name)) {
                collectFiles(fullPath, output);
            }
        // Если это файл нужного типа, добавляем к результату
        } else if (entry.isFile() && isTargetFile(entry.name)) {
            output.push(`\n==== Файл: ${fullPath} ====\n`);
            const content = fs.readFileSync(fullPath, 'utf-8');
            output.push(content);
        }
    }
}

function main(): void {
    // Используем ТЕКУЩУЮ директорию для парсинга
    const targetDir = process.cwd();
    const outputFile = path.join(targetDir, 'files-output.txt');

    // Проверяем существование директории
    if (!fs.existsSync(targetDir) || !fs.statSync(targetDir).isDirectory()) {
        console.error('Путь не найден или не является директорией:', targetDir);
        process.exit(1);
    }

    const result: string[] = [];
    collectFiles(targetDir, result);

    fs.writeFileSync(outputFile, result.join('\n'), 'utf-8');
    console.log(`Операция завершена. Результат сохранён в "${outputFile}"`);
}

main();