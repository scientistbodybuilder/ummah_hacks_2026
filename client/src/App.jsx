import { BrowserRouter as Router, Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { ArrowRight } from 'lucide-react'

function App() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
    // Add Google Fonts
    const link = document.createElement('link');
    link.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Sora:wght@400;500;600;700;800&display=swap';
    link.rel = 'stylesheet';
    document.head.appendChild(link);
  }, []);

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-teal-950 text-white" style={{ fontFamily: "'Inter', sans-serif" }}>
        {/* Navigation */}
        <nav className="fixed top-0 w-full bg-slate-950/90 backdrop-blur-md z-50 shadow-lg shadow-teal-500/10">
          <div className="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center">
            <div className="text-3xl font-bold bg-gradient-to-r from-teal-400 to-emerald-400 bg-clip-text text-transparent" style={{ fontFamily: "'Sora', sans-serif" }}>
              SHARAH
            </div>
            <div className="flex items-center gap-8">
              <a href="#about" className="text-slate-300 hover:text-teal-400 transition-colors font-medium">About</a>
              <a href="#demo" className="text-slate-300 hover:text-teal-400 transition-colors font-medium">Demo</a>
              <Link to="/dashboard">
                <button className="px-6 py-2.5 bg-gradient-to-r from-teal-500 to-emerald-500 rounded-lg font-semibold hover:shadow-lg hover:shadow-teal-500/50 transition-all duration-300 hover:scale-105">
                  Try Now
                </button>
              </Link>
            </div>
          </div>
          {/* Bottom border line */}
          <div className="h-0.5 bg-gradient-to-r from-transparent via-teal-500 to-transparent"></div>
        </nav>

        {/* Hero Section with Glass Effect */}
        <section className="pt-40 pb-24 px-6 min-h-screen flex items-center">
          <div className="max-w-7xl mx-auto w-full">
            <div className={`transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
              {/* Glass card container */}
              <div className="relative max-w-5xl mx-auto">
                <div className="absolute inset-0 bg-gradient-to-r from-teal-500/10 to-emerald-500/10 blur-2xl"></div>
                <div className="relative bg-slate-800/30 backdrop-blur-xl rounded-3xl p-12 lg:p-16 border border-slate-700/50 shadow-2xl">
                  
                  <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight" style={{ fontFamily: "'Sora', sans-serif" }}>
                    <span className="bg-gradient-to-r from-white via-teal-100 to-emerald-200 bg-clip-text text-transparent">
                      SHARAH
                    </span>
                    <br />
                    <span className="text-white">
                      Instant Shariah
                    </span>
                    <br />
                    <span className="bg-gradient-to-r from-teal-400 to-emerald-400 bg-clip-text text-transparent">
                      Compliance
                    </span>
                  </h1>
                  
                  <p className="text-lg md:text-xl text-slate-300 mb-10 leading-relaxed max-w-3xl">
                    Validate Islamic financial products in seconds, not weeks. Make confident halal investment decisions with precision.
                  </p>
                  
                  <div className="flex flex-col sm:flex-row gap-4 mb-12">
                    <Link to="/dashboard">
                      <button className="group px-8 py-4 bg-gradient-to-r from-teal-500 to-emerald-500 rounded-xl font-bold text-lg hover:shadow-2xl hover:shadow-teal-500/50 transition-all duration-300 hover:scale-105 flex items-center justify-center gap-2 w-full sm:w-auto">
                        Try SHARAH Now
                        <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                      </button>
                    </Link>
                    <a href="#demo">
                      <button className="px-8 py-4 bg-slate-800/50 backdrop-blur rounded-xl font-semibold text-lg border border-slate-700 hover:border-teal-500/50 transition-all duration-300 w-full sm:w-auto">
                        Watch Demo
                      </button>
                    </a>
                  </div>

                  {/* Quick stats */}
                  <div className="flex flex-wrap gap-8 pt-8 border-t border-slate-700/50">
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Video Section */}
        <section id="demo" className="py-20 px-4 sm:px-6 lg:px-8">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-bold text-center mb-12" style={{ fontFamily: "'Sora', sans-serif" }}>
              See <span className="bg-gradient-to-r from-teal-400 to-emerald-400 bg-clip-text text-transparent">SHARAH</span> in Action
            </h2>
            <div className="relative w-full rounded-2xl overflow-hidden shadow-2xl border border-slate-700/50" style={{ paddingBottom: '56.25%' }}>
              <iframe
                className="absolute top-0 left-0 w-full h-full"
                src="https://www.loom.com/embed/your-video-id"
                frameBorder="0"
                allowFullScreen
                title="SHARAH Demo Video"
              ></iframe>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section id="about" className="py-20 px-4 sm:px-6 lg:px-8">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-bold text-center mb-16" style={{ fontFamily: "'Sora', sans-serif" }}>
              Why Choose <span className="bg-gradient-to-r from-teal-400 to-emerald-400 bg-clip-text text-transparent">SHARAH</span>?
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {/* Feature 1 */}
              <div className="bg-slate-800/30 backdrop-blur-xl rounded-2xl p-8 border border-slate-700/50 hover:border-teal-500/50 transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-teal-500/20">
                <div className="text-5xl mb-4">⚡</div>
                <h3 className="text-2xl font-bold mb-3 text-white" style={{ fontFamily: "'Sora', sans-serif" }}>Instant</h3>
                <p className="text-slate-300">
                  Validate products in &lt;1 second, not 3-5 weeks
                </p>
              </div>

              {/* Feature 2 */}
              <div className="bg-slate-800/30 backdrop-blur-xl rounded-2xl p-8 border border-slate-700/50 hover:border-teal-500/50 transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-teal-500/20">
                <div className="text-5xl mb-4">🎯</div>
                <h3 className="text-2xl font-bold mb-3 text-white" style={{ fontFamily: "'Sora', sans-serif" }}>Accurate</h3>
                <p className="text-slate-300">
                  98% F1 score on Shariah compliance vs 60% for generic AI
                </p>
              </div>git checkout

              {/* Feature 3 */}
              <div className="bg-slate-800/30 backdrop-blur-xl rounded-2xl p-8 border border-slate-700/50 hover:border-teal-500/50 transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-teal-500/20">
                <div className="text-5xl mb-4">📊</div>
                <h3 className="text-2xl font-bold mb-3 text-white" style={{ fontFamily: "'Sora', sans-serif" }}>Transparent</h3>
                <p className="text-slate-300">
                  See which fatwas were checked, full audit trail
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="py-8 px-4 sm:px-6 lg:px-8 border-t border-teal-500/20">
          <div className="max-w-6xl mx-auto text-center text-slate-400">
            <div className="text-2xl font-bold bg-gradient-to-r from-teal-400 to-emerald-400 bg-clip-text text-transparent mb-2" style={{ fontFamily: "'Sora', sans-serif" }}>
              SHARAH
            </div>
            <p className="text-sm">&copy; 2026 SHARAH. Making Islamic finance accessible to all.</p>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App