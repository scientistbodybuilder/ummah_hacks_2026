import axios from "axios"
const API_URL = import.meta.env.VITE_API_URL
// console.log(API_URL)

export const uploadFile = async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    const dateTime = new Date().toLocaleString()
    const response = await axios.post(`${API_URL}/api/pipeline`, formData, {
        headers: {
            "Content-Type": "multipart/form-data"
        }
    });
    // console.log('file upload response:', response);
    if (response.status >= 200 && response.status < 300) {
        console.log("File analyzed successfully", response.data)
        let obj = {} as Record<string, any[]>
        const rulingData = response.data.data
        Object.keys(rulingData).forEach((ruling) => {
            obj[ruling] = rulingData[ruling].map((item: any) => ({
                chunk: item?.metadata.chunk,
                ruling: item?.metadata.ruling,
                confidence: item?.confidence,
                suggestion: item?.suggestion,
                summary: item?.summary,
                reasoning: item?.reasoning
            }))
        })
        //upload file key to session storage
        const key = `${file.name}-${dateTime}`
        //current keys
        const currentKeys = sessionStorage.getItem('recentUploads')
        const updatedKeys = currentKeys ? [...JSON.parse(currentKeys), key] : [key]
        sessionStorage.setItem('recentUploads', JSON.stringify(updatedKeys))
        return obj
    } else {
        throw new Error(response.data?.error || "Error analyzing file")
    }
}