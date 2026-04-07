#!/usr/bin/env bun
import Ajv from 'ajv';

const files: [`${string}.json`, string][] = [
    ['brutalplus.json', 'BrutalPlusList'],
    ['commandersummaries.json', 'CommanderList'],
];

const ajv = new Ajv();
for (const [file, type] of files) {
    const fileContent = await Bun.file(`source-data/${file}`).json();

    const fileSchema = await Bun.file(`source-data/schemas/${file.slice(0, -5)}.schema.json`).json();

    const validateFile = ajv.compile(fileSchema);
    if (!validateFile(fileContent)) {
        console.error(`${file} does not match schema:`);
        console.error(validateFile.errors);
        process.exit(1);
    }
}

console.log('All validations passed');
