import Link from 'next/link';

export default function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-dark-blue/80 backdrop-blur-sm">
      <nav className="container mx-auto px-6 py-4 flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold text-light-blue hover:text-white transition-colors">
          JARVIS
        </Link>
        <ul className="flex items-center space-x-6 text-light-slate">
          <li><Link href="/about" className="hover:text-light-blue transition-colors">Jarvis Haqida</Link></li>
          <li><Link href="/app-info" className="hover:text-light-blue transition-colors">Ilova</Link></li>
          <li><Link href="/download" className="font-bold text-light-blue border border-light-blue px-4 py-2 rounded hover:bg-light-blue hover:text-dark-blue transition-all">
            Yuklab Olish
          </Link></li>
        </ul>
      </nav>
    </header>
  );
}
