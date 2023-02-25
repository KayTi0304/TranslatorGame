import axios from "axios";

const url = "http://localhost:5000";

class ApiService {
    static async getTranslation(text, language) {
        console.log(text, ": ", language);
        return new Promise((resolve, reject) => {
            axios.post(`${url}/get-translation`, {
                    text: text,
                    language: language,
                })
                .then((res) => {
                    const data = res.data;
                    resolve(data);
                })
                .catch((err) => {
                    reject(err);
                });
        })
    }
}

export default ApiService;