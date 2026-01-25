import axios from 'axios'

/**
 * Analyze a PDF file for Shariah compliance
 * @param {File} file - The PDF file to analyze
 * @returns {Promise<Object>} - The analysis result
 */
export const analyzeDocument = async (file) => {
    if (!file) {
        throw new Error("No file provided")
    }

    const formData = new FormData()
    formData.append("file", file)

    const response = await axios.post('http://localhost:8000/analyze', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })

    if (response.status >= 200 && response.status < 300) {
        console.log("File analyzed successfully", response.data)
        return response.data
    } else {
        throw new Error(response.data?.detail || "Error analyzing file")
    }
}
