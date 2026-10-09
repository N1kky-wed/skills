import { describe, it } from 'node:test'
import assert from 'node:assert/strict'
import { readdirSync, readFileSync, statSync } from 'node:fs'
import { join, relative } from 'node:path'
import { fileURLToPath } from 'node:url'
import { createRequire } from 'node:module'
import type * as TS from 'typescript'

// TypeScript ships as CommonJS. Require it directly rather than fighting the
// ESM interop, the same way src/em-dash.test.mts does.
const require = createRequire(import.meta.url)
const ts = require('typescript') as typeof TS

/**
 * The palette's contrast rules, held mechanically.
 *
 * DESIGN.md states them and globals.css explains them, but a rule that lives
 * only in prose gets obeyed by whoever remembers it. This walks the syntax tree
 * of every source file and reads the class strings a component ships, the same
 * seam a browser reads them through, and fails on the three things the rules
 * forbid:
 *
 *   1. orange written as text with any token but accent-strong. `text-accent`
 *      on its own is 3.46:1 on cream; the decorative ramp (accent-light,
 *      accent-soft, accent-mid, accent-pale) is never a text colour at all.
 *      Allowlisted exceptions, per file and each with its reason: accent as
 *      text on an ink field, where it clears AA at 4.80, or accent on a glyph
 *      that is never a letter, where the 3:1 non-text floor applies.
 *   2. an arbitrary hex colour class (`bg-[#...]`), which is a token nobody
 *      named and a contrast pair nobody measured.
 *   3. an arbitrary font size (`text-[0.8125rem]`), which is a step the type
 *      scale does not have. Add the step, then use it.
 *   4. a dark band rule or fill written as text. `line-dark` is 1.46:1 on ink
 *      and `surface-dark` 1.12:1; they draw a border and a raised step on an
 *      ink field and nothing can be read off either.
 *   5. `on-dark-muted` written as text outside a file that declares itself an
 *      ink field. It clears AA on ink (6.26) and on surface-dark (5.57) and
 *      fails everywhere else (2.65 on cream), so, like accent on ink, each
 *      file that writes it is allowlisted with the reason.
 *
 * Comments are structurally absent from the walk, so a decision can still be
 * explained in one. Tests are skipped: this file names every pattern it hunts
 * as data, and a spec never ships a class string.
 */
const SRC = fileURLToPath(new URL('.', import.meta.url))

/**
 * A per file exception to one rule: a claim about every use of a class in
 * that file, with the reason spelled out, checked below to still be in use.
 */
type PaletteClaim = { file: string; why: string }

/**
 * Where `text-accent` (the fill, not accent-strong) may be written as a colour
 * class. Each entry is a claim about every such class in that file, and needs
 * the reason spelled out: either the text sits on an ink field, where accent
 * clears AA at 4.80, or the class colours a glyph and never a letter, where the
 * 3:1 floor for a non-text mark applies (accent is 3.73 on surface and 3.46 on
 * cream).
 *
 * Dark bands are the same ink-field case, reached a different way. A redesigned
 * screen that lays orange text on an ink band (or on a caller-set ink tone, as
 * the brand mark does) is correct in accent, not accent-strong: accent-strong
 * drops to 3.66 on ink and fails, base accent clears at 4.80. The honest input
 * would be the resolved pairing, colour on background, but the ground is never
 * in the class string this walk reads: it is an ancestor's bg on another line,
 * or, for the brand mark, the caller's tone prop feeding a cva variant, so no
 * class in the file itself reveals it. So these ride the same per-file
 * allowlist as the rest, each with the ground it sits on named.
 */
const ACCENT_TEXT_EXCEPTIONS: readonly PaletteClaim[] = [
	{
		file: 'components/landing/site-footer.tsx',
		why: 'link hover on the ink bands, accent on ink is 4.80'
	},
	{
		file: 'components/app-shell/nav-item.tsx',
		why: 'the selected row glyph, a 16px mark on surface or cream, 3.73 and 3.46 against a 3:1 floor'
	},
	{
		file: 'components/landing/how-it-works-pinned.tsx',
		why: 'the eyebrow on the ink band, accent on ink is 4.80'
	},
	{
		file: 'components/landing/testimonial-wall.tsx',
		why: 'the eyebrow on the ink testimonials band, accent on ink is 4.80'
	},
	{
		file: 'components/landing/testimonial-mascot.tsx',
		why: 'the accent mascot crest, a glyph and never a letter, against the 3:1 non-text floor'
	},
	{
		file: 'components/landing/trust-and-control.tsx',
		why: 'the never-do eyebrow on the ink rules-box header, accent on ink is 4.80'
	},
	{
		file: 'components/brand/results/results-hero.tsx',
		why: 'the engagements figure on the ink results hero, accent on ink is 4.80'
	},
	{
		file: 'components/dashboard-queue/queue-card.tsx',
		why: 'the Up next eyebrow on the ink card, accent on ink is 4.80'
	},
	{
		file: 'components/creator/submissions/earnings-panel.tsx',
		why: 'the still-accruing figure on the ink money panel, accent on ink is 4.80'
	},
	{
		file: 'components/brand-mark.tsx',
		why: 'the 8x logotype in its ink-tone lockup, accent on ink is 4.80; the ground is the caller-set tone, not a class in this file'
	},
	{
		file: 'components/brand/profile/community-rail.tsx',
		why: 'the hand-read count on the ink community rail, accent on ink is 4.80'
	},
	{
		file: 'components/creator/reddit-account/eligibility-panel.tsx',
		why: 'the u/ mark, the met tick and the shortfall figure on the ink eligibility card, accent on ink is 4.80'
	},
	{
		file: 'components/auth/sign-up-confirmation.tsx',
		why: 'the eyebrow on the ink confirmation card, accent on ink is 4.80'
	}
]

/**
 * Where `text-on-dark-muted` may be written. The same shape of claim: every
 * use in the file sits on ink or on surface-dark.
 */
const ON_DARK_MUTED_ON_INK: readonly PaletteClaim[] = [
	{
		file: 'components/admin/attention.tsx',
		why: 'the breakdown line under the Today ink band headline, 6.26 on ink'
	},
	{
		file: 'components/landing/how-it-works-pinned.tsx',
		why: 'stage copy, spine labels and the Sample badge on the ink band, 6.26 on ink and 5.57 on surface-dark'
	},
	{
		file: 'components/landing/testimonial-wall.tsx',
		why: 'the intro on the ink band, 6.26 on ink'
	},
	{
		file: 'components/landing/testimonial-card.tsx',
		why: 'the quote and role on a default card, 6.26 on ink and 5.57 on surface-dark'
	},
	{
		file: 'components/brand/results/results-hero.tsx',
		why: 'the labels, help and timeline on the ink results hero and its tiles, 6.26 on ink and 5.57 on surface-dark'
	},
	{
		file: 'components/dashboard-queue/queue-card.tsx',
		why: 'the eyebrow separator and the up-next hint on the ink card, 6.26 on ink'
	},
	{
		file: 'components/creator/submissions/pipeline-strip.tsx',
		why: 'the holder word under a stage held by someone else, on the ink chevron, 6.26 on ink'
	},
	{
		file: 'components/creator/submissions/earnings-panel.tsx',
		why: 'the labels and the paid-out figure on the ink money panel, 6.26 on ink'
	},
	{
		file: 'components/auth/sign-up-confirmation.tsx',
		why: 'the body and the upcoming step labels on the ink confirmation card, 6.26 on ink'
	},
	{
		file: 'components/brand/profile/community-rail.tsx',
		why: 'every eyebrow, sub-label and note on the ink community rail, 6.26 on ink'
	},
	{
		file: 'components/creator/reddit-account/eligibility-panel.tsx',
		why: 'the check sub-labels, the of-bar caption and the not-read line on the ink eligibility card, 6.26 on ink'
	}
]

const RULES: readonly { name: string; pattern: RegExp; allow?: (rel: string) => boolean }[] = [
	{
		name: 'orange as text is accent-strong only',
		// text-accent, or text-accent-light/soft/mid/pale, with or without a
		// variant prefix and an opacity suffix. text-accent-strong and
		// text-accent-ink are the two legitimate spellings and are not matched.
		pattern: /(?<![\w-])(?:[\w-]+:)*text-accent(?:-(?:light|soft|mid|pale))?(?![\w-])/,
		allow: (rel) => ACCENT_TEXT_EXCEPTIONS.some((e) => e.file === rel)
	},
	{
		name: 'no arbitrary hex colour class',
		pattern: /(?<![\w-])(?:[\w-]+:)*[a-z-]+-\[#[0-9a-fA-F]{3,8}\]/
	},
	{
		name: 'no arbitrary font size',
		pattern: /(?<![\w-])(?:[\w-]+:)*text-\[[0-9.]+(?:rem|px|em)\]/
	},
	{
		name: 'a dark band rule or fill is never text',
		pattern: /(?<![\w-])(?:[\w-]+:)*text-(?:line-dark|surface-dark)(?![\w-])/
	},
	{
		name: 'on-dark-muted is text on an ink field only',
		pattern: /(?<![\w-])(?:[\w-]+:)*text-on-dark-muted(?![\w-])/,
		allow: (rel) => ON_DARK_MUTED_ON_INK.some((e) => e.file === rel)
	}
]

function walk({ dir, out = [] }: { dir: string; out?: string[] }): string[] {
	for (const entry of readdirSync(dir)) {
		if (entry === 'node_modules' || entry === '.next') continue
		const full = join(dir, entry)
		if (statSync(full).isDirectory()) walk({ dir: full, out })
		else if (/\.tsx?$/.test(entry) && !/\.test\.tsx?$/.test(entry)) out.push(full)
	}
	return out
}

/** Every string a component could hand to className, with its line number. */
function classStrings({
	source,
	fileName
}: {
	source: string
	fileName: string
}): { line: number; text: string }[] {
	const sf = ts.createSourceFile(
		fileName,
		source,
		ts.ScriptTarget.Latest,
		true,
		fileName.endsWith('.tsx') ? ts.ScriptKind.TSX : ts.ScriptKind.TS
	)
	const out: { line: number; text: string }[] = []
	const visit = (node: TS.Node) => {
		if (
			ts.isStringLiteral(node) ||
			ts.isNoSubstitutionTemplateLiteral(node) ||
			ts.isTemplateHead(node) ||
			ts.isTemplateMiddle(node) ||
			ts.isTemplateTail(node)
		) {
			out.push({ line: sf.getLineAndCharacterOfPosition(node.getStart(sf)).line, text: node.text })
		}
		ts.forEachChild(node, visit)
	}
	visit(sf)
	return out
}

describe('class strings obey the palette rules', () => {
	for (const rule of RULES) {
		it(rule.name, () => {
			const offenders: string[] = []
			for (const file of walk({ dir: SRC })) {
				const rel = relative(SRC, file).replace(/\\/g, '/')
				if (rule.allow?.(rel)) continue
				const source = readFileSync(file, 'utf8')
				for (const s of classStrings({ source, fileName: rel })) {
					const match = rule.pattern.exec(s.text)
					if (match) offenders.push(`${rel}:${s.line + 1}  ${match[0]}`)
				}
			}
			assert.deepEqual(
				offenders,
				[],
				`See DESIGN.md section 2 for the pairing that replaces it.\n${offenders.join('\n')}`
			)
		})
	}

	it('each exception list names files that still exist and still use the class', () => {
		// Read through the same walk as the rule, so a comment that merely mentions
		// the class cannot keep an entry alive.
		const claims: readonly {
			className: string
			claim: string
			entries: readonly PaletteClaim[]
		}[] = [
			{
				className: 'text-accent',
				claim: 'accent as a colour class',
				entries: ACCENT_TEXT_EXCEPTIONS
			},
			{
				className: 'text-on-dark-muted',
				claim: 'on-dark-muted on an ink field',
				entries: ON_DARK_MUTED_ON_INK
			}
		]
		for (const { className, claim, entries } of claims) {
			const bare = new RegExp(`(?<![\\w-])(?:[\\w-]+:)*${className}(?![\\w-])`)
			for (const entry of entries) {
				const source = readFileSync(join(SRC, entry.file), 'utf8')
				const strings = classStrings({ source, fileName: entry.file })
				assert.ok(
					strings.some((item) => bare.test(item.text)),
					`${entry.file} is allowlisted for ${claim} but no longer writes ${className}; drop the entry`
				)
			}
		}
	})
})
