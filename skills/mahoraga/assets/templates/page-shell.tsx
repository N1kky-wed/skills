// mahoraga template: route transitions with React's ViewTransition (Next 16 App Router, no config). CSS: motion.css.
import { ViewTransition } from 'react'

// Wraps each page so a route change animates: the page you leave sinks, the next one rises (globals.css, `.page`).
// It lives in every page rather than the layout, because a layout persists and would never enter or exit.
export function PageShell({ children, footer }: { children: React.ReactNode; footer?: React.ReactNode }) {
	return (
		<ViewTransition enter="page" exit="page" default="none">
			<div>
				<main>{children}</main>
				{footer}
			</div>
		</ViewTransition>
	)
}
