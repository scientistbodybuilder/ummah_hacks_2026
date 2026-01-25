import { Link } from 'react-router-dom'

function Landing() {
  return (
    <div className="min-h-screen bg-slate-900 text-white">
      {/* Navigation */}
      <nav className="w-full py-6 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="text-2xl font-bold text-teal-500">SHARAH</div>
          <Link
            to="/dashboard"
            className="px-6 py-2 bg-teal-500 hover:bg-teal-600 text-white font-semibold rounded-lg transition-colors duration-200"
          >
            Try Now
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 rounded-2xl p-8 sm:p-12 lg:p-16">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-6 text-white">
              SHARAH: Instant Shariah Compliance
            </h1>
            <p className="text-xl sm:text-2xl text-slate-300 mb-8 max-w-2xl mx-auto">
              Validate Islamic financial products in seconds, not weeks.
            </p>
            <Link
              to="/dashboard"
              className="inline-block px-8 py-4 bg-teal-500 hover:bg-teal-600 text-white font-semibold rounded-lg text-lg transition-colors duration-200 shadow-lg hover:shadow-xl"
            >
              Try SHARAH Now
            </Link>
          </div>
        </div>
      </section>

      {/* Video Section */}
      <section className="py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <div className="relative w-full rounded-xl overflow-hidden shadow-2xl" style={{ paddingBottom: '56.25%' }}>
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
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
            {/* Feature 1 */}
            <div className="bg-slate-700 rounded-xl p-6 lg:p-8 shadow-lg hover:shadow-xl transition-shadow duration-200">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="text-xl font-bold mb-3 text-white">Instant</h3>
              <p className="text-slate-300">
                Validate products in &lt;1 second, not 3-5 weeks
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-slate-700 rounded-xl p-6 lg:p-8 shadow-lg hover:shadow-xl transition-shadow duration-200">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-bold mb-3 text-white">Accurate</h3>
              <p className="text-slate-300">
                98% F1 score on Shariah compliance vs 60% for generic AI
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-slate-700 rounded-xl p-6 lg:p-8 shadow-lg hover:shadow-xl transition-shadow duration-200">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-xl font-bold mb-3 text-white">Transparent</h3>
              <p className="text-slate-300">
                See which fatwas were checked, full audit trail
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-4 sm:px-6 lg:px-8 border-t border-slate-800">
        <div className="max-w-4xl mx-auto text-center text-slate-400">
          <p>&copy; 2026 SHARAH. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}

export default Landing
