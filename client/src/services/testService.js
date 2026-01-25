import axios from 'axios'

export const handleFileChange = async (e) => {
    const file = e.target.files[0]
    console.log(file)
    const formData = new FormData()
    formData.append("file", file)
    try {
        const response = await axios.post('http://localhost:8000/analyze', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        console.log(response)
        if (response.status >= 200 && response.status < 300) {
            console.log("File uploaded successfully", response.data)
        } else {
            console.log("Error uploading file", response.data)
        }
    } catch (err) {
        console.log("Error uploading file", err)
    }

}
