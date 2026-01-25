import { useState, useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import {
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  CircularProgress,
  Snackbar,
  Alert,
  ThemeProvider,
  createTheme,
} from '@mui/material'
import CloudUploadIcon from '@mui/icons-material/CloudUpload'
import VisibilityIcon from '@mui/icons-material/Visibility'
import { uploadPDF, getApplications } from '../services/api'

// Custom dark theme to match landing page
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#14b8a6', // teal-500
    },
    background: {
      default: '#0f172a', // slate-900
      paper: '#334155', // slate-700
    },
  },
  components: {
    MuiTableCell: {
      styleOverrides: {
        root: {
          borderColor: '#475569', // slate-600
        },
        head: {
          backgroundColor: '#1e293b', // slate-800
          color: '#f1f5f9', // slate-100
          fontWeight: 600,
        },
      },
    },
    MuiTableRow: {
      styleOverrides: {
        root: {
          '&:hover': {
            backgroundColor: '#475569 !important', // slate-600
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
      },
    },
  },
})

function Dashboard() {
  const [applications, setApplications] = useState([])
  const [loading, setLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' })
  const fileInputRef = useRef(null)

  // Fetch applications on mount
  useEffect(() => {
    fetchApplications()
  }, [])

  const fetchApplications = async () => {
    setLoading(true)
    try {
      const data = await getApplications()
      setApplications(data)
    } catch (error) {
      console.error('Error fetching applications:', error)
      setSnackbar({
        open: true,
        message: 'Failed to fetch applications',
        severity: 'error',
      })
    } finally {
      setLoading(false)
    }
  }

  const handleUploadClick = () => {
    fileInputRef.current?.click()
  }

  const handleFileChange = async (event) => {
    const file = event.target.files?.[0]
    if (!file) return

    if (!file.name.endsWith('.pdf')) {
      setSnackbar({
        open: true,
        message: 'Please select a PDF file',
        severity: 'error',
      })
      return
    }

    setUploading(true)
    try {
      const newApplication = await uploadPDF(file)
      setApplications((prev) => [newApplication, ...prev])
      setSnackbar({
        open: true,
        message: 'PDF uploaded successfully!',
        severity: 'success',
      })
    } catch (error) {
      console.error('Error uploading PDF:', error)
      setSnackbar({
        open: true,
        message: error.response?.data?.detail || 'Failed to upload PDF',
        severity: 'error',
      })
    } finally {
      setUploading(false)
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  const handleCloseSnackbar = () => {
    setSnackbar((prev) => ({ ...prev, open: false }))
  }

  const handleInspect = (id) => {
    // Navigate to inspect page (to be implemented)
    console.log('Inspecting application:', id)
  }

  return (
    <ThemeProvider theme={darkTheme}>
      <div className="min-h-screen bg-slate-900 text-white">
        {/* Navigation */}
        <nav className="w-full py-6 px-4 sm:px-6 lg:px-8">
          <div className="max-w-6xl mx-auto flex items-center justify-between">
            <Link to="/" className="text-2xl font-bold text-teal-500">
              SHARAH
            </Link>
            <div className="text-slate-300">Dashboard</div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="px-4 sm:px-6 lg:px-8 pb-16">
          <div className="max-w-6xl mx-auto">
            {/* Upload Section */}
            <section className="mb-8">
              <div className="bg-slate-800 rounded-xl p-6 shadow-lg">
                <h2 className="text-xl font-semibold mb-4">Upload Financial Product Document</h2>
                <p className="text-slate-400 mb-4">
                  Upload a PDF document to validate its Shariah compliance.
                </p>
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileChange}
                  accept=".pdf"
                  className="hidden"
                />
                <Button
                  variant="contained"
                  startIcon={uploading ? <CircularProgress size={20} color="inherit" /> : <CloudUploadIcon />}
                  onClick={handleUploadClick}
                  disabled={uploading}
                  sx={{
                    backgroundColor: '#14b8a6',
                    '&:hover': {
                      backgroundColor: '#0d9488',
                    },
                    textTransform: 'none',
                    fontWeight: 600,
                    padding: '12px 24px',
                    fontSize: '1rem',
                  }}
                >
                  {uploading ? 'Uploading...' : 'Upload PDF'}
                </Button>
              </div>
            </section>

            {/* Applications Table */}
            <section>
              <h2 className="text-xl font-semibold mb-4">Your Applications</h2>
              {loading ? (
                <div className="flex justify-center py-12">
                  <CircularProgress sx={{ color: '#14b8a6' }} />
                </div>
              ) : applications.length === 0 ? (
                <div className="bg-slate-800 rounded-xl p-8 text-center">
                  <p className="text-slate-400">No applications yet. Upload a PDF to get started.</p>
                </div>
              ) : (
                <TableContainer
                  component={Paper}
                  sx={{
                    backgroundColor: '#334155',
                    borderRadius: '12px',
                    overflow: 'hidden',
                  }}
                >
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Application ID</TableCell>
                        <TableCell>Application Name</TableCell>
                        <TableCell>Date</TableCell>
                        <TableCell align="center">Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {applications.map((app) => (
                        <TableRow key={app.id}>
                          <TableCell sx={{ color: '#f1f5f9', fontFamily: 'monospace' }}>
                            {app.id}
                          </TableCell>
                          <TableCell sx={{ color: '#f1f5f9' }}>{app.name}</TableCell>
                          <TableCell sx={{ color: '#94a3b8' }}>{app.date}</TableCell>
                          <TableCell align="center">
                            <Button
                              variant="outlined"
                              size="small"
                              startIcon={<VisibilityIcon />}
                              onClick={() => handleInspect(app.id)}
                              sx={{
                                borderColor: '#14b8a6',
                                color: '#14b8a6',
                                '&:hover': {
                                  borderColor: '#0d9488',
                                  backgroundColor: 'rgba(20, 184, 166, 0.1)',
                                },
                                textTransform: 'none',
                              }}
                            >
                              Inspect
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </section>
          </div>
        </main>

        {/* Footer */}
        <footer className="py-8 px-4 sm:px-6 lg:px-8 border-t border-slate-800">
          <div className="max-w-6xl mx-auto text-center text-slate-400">
            <p>&copy; 2026 SHARAH. All rights reserved.</p>
          </div>
        </footer>

        {/* Snackbar for notifications */}
        <Snackbar
          open={snackbar.open}
          autoHideDuration={6000}
          onClose={handleCloseSnackbar}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        >
          <Alert
            onClose={handleCloseSnackbar}
            severity={snackbar.severity}
            sx={{ width: '100%' }}
          >
            {snackbar.message}
          </Alert>
        </Snackbar>
      </div>
    </ThemeProvider>
  )
}

export default Dashboard
