// This is a minimal root layout that redirects to the [lang] dynamic route
// The actual layout logic is in app/[lang]/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
