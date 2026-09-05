import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"

import './index.css'
import App from './App.tsx'

const queryClient = new QueryClient()
queryClient.setQueryDefaults(['analysis'], { gcTime: Infinity })
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </StrictMode>,
)
