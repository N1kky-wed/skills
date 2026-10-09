// mahoraga template: a heading line set word by word; each word rises as the heading crosses the viewport.
// Put data-reveal="words" on the heading (motion.css). offset continues the stagger across lines.
// A line set word by word, each word rising as the heading crosses the viewport (globals.css, data-reveal="words").
export function Words({ text, className, offset = 0 }: { text: string; className?: string; offset?: number }) {
	return (
		<span className={className}>
			{text.split(' ').map((word, i) => (
				<span key={`${word}-${i}`} style={{ ['--w' as string]: offset + i }}>
					{word}
					{i < text.split(' ').length - 1 ? ' ' : ''}
				</span>
			))}
		</span>
	)
}
