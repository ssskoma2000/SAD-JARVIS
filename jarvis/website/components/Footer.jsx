export default function Footer() {
  return (
    <footer className="relative z-20 bg-dark-blue border-t border-slate/20">
      <div className="container mx-auto px-6 py-4 text-center text-slate">
        <p>&copy; {new Date().getFullYear()} Jarvis Project by Koma @ iTech.</p>
      </div>
    </footer>
  );
}
