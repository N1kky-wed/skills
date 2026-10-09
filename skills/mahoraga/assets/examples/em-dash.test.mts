import { describe, it } from 'node:test'
import assert from 'node:assert/strict'
import { readdirSync, readFileSync, statSync, existsSync } from 'node:fs'
import { join, relative } from 'node:path'
import { fileURLToPath } from 'node:url'
import { createRequire } from 'node:module'
import type * as TS from 'typescript'

// TypeScript ships as CommonJS. Require it directly rather than fighting the
// ESM interop, which is what made the compiler namespace come back undefined
// under other runners.
const require = createRequire(import.meta.url)
const ts = require('typescript') as typeof TS

/**
 * No em dash reaches a reader.
 *
 * A style note only gets obeyed by whoever already remembers it, so this is a
 * test instead. It walks the syntax tree of every source file and fails if the
 * character sits in text a reader sees: string literals, template text, and JSX
 * text. Comments and regex literals are structurally absent from the walk, so a
 * decision can still be explained in a comment. It also scans the i18n message
 * catalogs, which is where this app's user-facing copy actually lives.
 *
 * The character is referenced by code point on purpose, so this guard holds no
 * literal em dash of its own and needs no self exemption.
 */
const HERE = fileURLToPath(new URL('.', import.meta.url))
const SRC = HERE
const MESSAGES = join(HERE, '..', 'messages')
const EM_DASH = String.fromCharCode(0x2014)

/** The HTML entity forms, which the build decodes to a real em dash in JSX text. */
const ENTITY = /&(?:mdash|#8212|#x2014);/gi

/**
 * Lines that may legitimately hold the character, by exact file and substring.
 * Empty for now. A new entry is a claim that the rule does not apply and needs a
 * reason. Matched on the trimmed line so reindenting cannot widen it.
 */
const ALLOWED: readonly { file: string; contains: string; why: string }[] = []

function walk(dir: string, out: string[] = []): string[] {
	for (const entry of readdirSync(dir)) {
		if (entry === 'node_modules' || entry === '.next') continue
		const full = join(dir, entry)
		if (statSync(full).isDirectory()) walk(full, out)
		else if (/\.tsx?$/.test(entry)) out.push(full)
	}
	return out
}

/** Zero-based line numbers where the character sits in rendered text. */
function renderedDashLines(source: string, fileName: string): number[] {
	const sf = ts.createSourceFile(
		fileName,
		source,
		ts.ScriptTarget.Latest,
		true,
		fileName.endsWith('.tsx') ? ts.ScriptKind.TSX : ts.ScriptKind.TS
	)

	const lines: number[] = []

	const record = (node: TS.Node, alsoEntities: boolean) => {
		const raw = node.getText(sf)
		const start = node.getStart(sf)
		for (let i = raw.indexOf(EM_DASH); i !== -1; i = raw.indexOf(EM_DASH, i + 1)) {
			lines.push(sf.getLineAndCharacterOfPosition(start + i).line)
		}
		if (!alsoEntities) return
		ENTITY.lastIndex = 0
		for (let m = ENTITY.exec(raw); m; m = ENTITY.exec(raw)) {
			lines.push(sf.getLineAndCharacterOfPosition(start + m.index).line)
		}
	}

	const visit = (node: TS.Node) => {
		if (
			ts.isStringLiteral(node) ||
			ts.isNoSubstitutionTemplateLiteral(node) ||
			ts.isTemplateHead(node) ||
			ts.isTemplateMiddle(node) ||
			ts.isTemplateTail(node) ||
			ts.isJsxText(node)
		) {
			record(node, ts.isJsxText(node))
		}
		ts.forEachChild(node, visit)
	}
	visit(sf)

	return lines
}

function allowed(rel: string, line: string): boolean {
	return ALLOWED.some((e) => rel === e.file && (e.contains === '' || line.includes(e.contains)))
}

/** Every string value in a parsed JSON tree, with a dotted key path. */
function jsonStrings(value: unknown, path: string, out: { path: string; text: string }[]) {
	if (typeof value === 'string') out.push({ path, text: value })
	else if (Array.isArray(value)) value.forEach((v, i) => jsonStrings(v, `${path}[${i}]`, out))
	else if (value && typeof value === 'object') {
		for (const [k, v] of Object.entries(value)) jsonStrings(v, path ? `${path}.${k}` : k, out)
	}
}

describe('rendered copy carries no em dash', () => {
	it('finds none in source outside the argued exemptions', () => {
		const offenders: string[] = []

		for (const file of walk(SRC)) {
			const rel = relative(SRC, file).replace(/\\/g, '/')
			const source = readFileSync(file, 'utf8')
			ENTITY.lastIndex = 0
			if (!source.includes(EM_DASH) && !ENTITY.test(source)) continue

			const srcLines = source.split('\n')
			for (const line of new Set(renderedDashLines(source, rel))) {
				const raw = (srcLines[line] ?? '').trim()
				if (allowed(rel, raw)) continue
				offenders.push(`${rel}:${line + 1}  ${raw.slice(0, 110)}`)
			}
		}

		assert.deepEqual(offenders, [], `Use a period or a comma instead.\n${offenders.join('\n')}`)
	})

	it('finds none in the message catalogs', () => {
		if (!existsSync(MESSAGES)) return
		const offenders: string[] = []
		for (const entry of readdirSync(MESSAGES)) {
			if (!entry.endsWith('.json')) continue
			const strings: { path: string; text: string }[] = []
			jsonStrings(JSON.parse(readFileSync(join(MESSAGES, entry), 'utf8')), '', strings)
			for (const s of strings) {
				if (s.text.includes(EM_DASH) || ENTITY.test(s.text)) {
					offenders.push(`messages/${entry}  ${s.path}`)
				}
				ENTITY.lastIndex = 0
			}
		}
		assert.deepEqual(offenders, [], `Use a period or a comma instead.\n${offenders.join('\n')}`)
	})

	it('detects a real one in a plain string', () => {
		const withDash = `const s = "a ${EM_DASH} b";`
		assert.deepEqual(renderedDashLines(withDash, 'synthetic.ts'), [0])
	})

	it('sees an em dash written as an HTML entity in JSX text', () => {
		const jsx = `export const A = () => <p>rate &mdash; never estimates</p>;`
		assert.deepEqual(renderedDashLines(jsx, 'synthetic.tsx'), [0])
	})

	it('leaves an entity in a plain string alone', () => {
		assert.deepEqual(renderedDashLines(`const s = "&mdash;";`, 'synthetic.ts'), [])
	})
})
