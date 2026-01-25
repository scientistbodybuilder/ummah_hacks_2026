import { useState, useRef } from 'react'
import { BrowserRouter as Router, Link } from 'react-router-dom'
import { analyzeDocument } from './services/testService'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const fileInputRef = useRef(null)

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      setSelectedFile(file)
      setResult(null)
      setError(null)
    }
  }

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError("Please select a PDF file first")
      return
    }

    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await analyzeDocument(selectedFile)
      setResult(data.result)
    } catch (err) {
      console.error("Analysis error:", err)
      setError(err.response?.data?.detail || err.message || "Failed to analyze document")
    } finally {
      setIsLoading(false)
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    e.stopPropagation()
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    const file = e.dataTransfer.files[0]
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file)
      setResult(null)
      setError(null)
    } else {
      setError("Please drop a PDF file")
    }
  }

  const clearFile = () => {
    setSelectedFile(null)
    setResult(null)
    setError(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const getSuggestionStyles = (suggestion) => {
    switch (suggestion) {
      case 'compliant':
        return 'bg-green-500/20 text-green-400 border-green-500/50'
      case 'non-compliant':
        return 'bg-red-500/20 text-red-400 border-red-500/50'
      default:
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/50'
    }
  }

  const getSeverityStyles = (severity) => {
    switch (severity) {
      case 'high':
        return 'bg-red-500/20 text-red-400'
      case 'medium':
        return 'bg-yellow-500/20 text-yellow-400'
      case 'low':
        return 'bg-blue-500/20 text-blue-400'
      default:
        return 'bg-slate-500/20 text-slate-400'
    }
  }

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-teal-950 text-white" style={{ fontFamily: "'Inter', sans-serif" }}>
        {/* Navigation */}
        <nav className="w-full py-6 px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto flex items-center justify-between">
            <div className="text-2xl font-bold text-teal-500">SHARAH</div>
            <Link
              to="/dashboard"
              className="px-6 py-2 bg-teal-500 hover:bg-teal-600 text-white font-semibold rounded-lg transition-colors duration-200"
            >
              Dashboard
            </Link>
          </div>
          {/* Bottom border line */}
          <div className="h-0.5 bg-gradient-to-r from-transparent via-teal-500 to-transparent"></div>
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

              {/* File Upload Section */}
              <div className="max-w-xl mx-auto mb-8">
                <div
                  onDragOver={handleDragOver}
                  onDrop={handleDrop}
                  onClick={() => fileInputRef.current?.click()}
                  className={`relative border-2 border-dashed rounded-xl p-8 transition-all duration-200 cursor-pointer
                    ${selectedFile 
                      ? 'border-teal-500 bg-teal-500/10' 
                      : 'border-slate-600 hover:border-teal-500 hover:bg-slate-800/50'
                    }`}
                >
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".pdf"
                    onChange={handleFileSelect}
                    className="hidden"
                  />
                  
                  {selectedFile ? (
                    <div className="flex items-center justify-center gap-3">
                      <svg className="w-8 h-8 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      <div className="text-left">
                        <p className="text-white font-medium">{selectedFile.name}</p>
                        <p className="text-slate-400 text-sm">{(selectedFile.size / 1024).toFixed(1)} KB</p>
                      </div>
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          clearFile()
                        }}
                        className="ml-4 p-1 hover:bg-slate-700 rounded-full transition-colors"
                      >
                        <svg className="w-5 h-5 text-slate-400 hover:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                  ) : (
                    <div className="text-center">
                      <svg className="w-12 h-12 mx-auto text-slate-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                      <p className="text-slate-300 mb-2">Drag & drop your PDF here, or click to browse</p>
                      <p className="text-slate-500 text-sm">Supports PDF files only</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Analyze Button */}
              <button
                onClick={handleAnalyze}
                disabled={!selectedFile || isLoading}
                className={`inline-flex items-center justify-center gap-2 px-8 py-4 font-semibold rounded-lg text-lg transition-all duration-200 shadow-lg
                  ${selectedFile && !isLoading
                    ? 'bg-teal-500 hover:bg-teal-600 text-white hover:shadow-xl'
                    : 'bg-slate-700 text-slate-400 cursor-not-allowed'
                  }`}
              >
                {isLoading ? (
                  <>
                    <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                    </svg>
                    Try SHARAH Now
                  </>
                )}
              </button>

              {/* Error Message */}
              {error && (
                <div className="mt-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-400">
                  <div className="flex items-center gap-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {error}
                  </div>
                </div>
              )}

              {/* Results Section */}
              {result && (
                <div className="mt-8 text-left">
                  <div className="bg-slate-800/80 rounded-xl p-6 border border-slate-700">
                    {/* Header with Verdict */}
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6 pb-6 border-b border-slate-700">
                      <div>
                        <h3 className="text-xl font-bold text-white mb-1">Analysis Results</h3>
                        <p className="text-slate-400 text-sm">Shariah Compliance Assessment</p>
                      </div>
                      <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full border ${getSuggestionStyles(result.suggestion)}`}>
                        {result.suggestion === 'compliant' && (
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        )}
                        {result.suggestion === 'non-compliant' && (
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        )}
                        {result.suggestion === 'uncertain' && (
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        )}
                        <span className="font-semibold capitalize">{result.suggestion}</span>
                      </div>
                    </div>

                    {/* Confidence Score */}
                    <div className="mb-6">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-slate-400 text-sm">Confidence Score</span>
                        <span className="text-white font-semibold">{result.confidence}%</span>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full transition-all duration-500 ${
                            result.confidence >= 70 ? 'bg-green-500' : 
                            result.confidence >= 40 ? 'bg-yellow-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${result.confidence}%` }}
                        />
                      </div>
                    </div>

                    {/* Summary */}
                    <div className="mb-6">
                      <h4 className="text-white font-semibold mb-2 flex items-center gap-2">
                        <svg className="w-4 h-4 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Summary
                      </h4>
                      <p className="text-slate-300 leading-relaxed">{result.summary}</p>
                    </div>

                    {/* Issues */}
                    {result.issues && result.issues.length > 0 && (
                      <div className="mb-6">
                        <h4 className="text-white font-semibold mb-3 flex items-center gap-2">
                          <svg className="w-4 h-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                          </svg>
                          Issues Found ({result.issues.length})
                        </h4>
                        <div className="space-y-3">
                          {result.issues.map((issue, index) => (
                            <div key={index} className="bg-slate-700/50 rounded-lg p-4">
                              <div className="flex items-start justify-between gap-4">
                                <div className="flex-1">
                                  <div className="flex items-center gap-2 mb-1">
                                    <span className="text-white font-medium capitalize">{issue.principle}</span>
                                    <span className={`text-xs px-2 py-0.5 rounded-full ${getSeverityStyles(issue.severity)}`}>
                                      {issue.severity}
                                    </span>
                                  </div>
                                  <p className="text-slate-400 text-sm">{issue.description}</p>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Detailed Reasoning */}
                    <div>
                      <h4 className="text-white font-semibold mb-2 flex items-center gap-2">
                        <svg className="w-4 h-4 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                        </svg>
                        Detailed Reasoning
                      </h4>
                      <p className="text-slate-300 leading-relaxed whitespace-pre-wrap">{result.reasoning}</p>
                    </div>

                    {/* Metadata */}
                    {result._metadata && (
                      <div className="mt-6 pt-6 border-t border-slate-700">
                        <p className="text-slate-500 text-xs">
                          Analyzed using {result._metadata.total_chunks_matched} knowledge base chunks | Model: {result._metadata.model_used}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              )}
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