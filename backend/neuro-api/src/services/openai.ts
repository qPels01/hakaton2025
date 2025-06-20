import axios from 'axios';

const OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions';

export async function askChatGPT(messages: any[], apiKey: string) {
    try {
        const response = await axios.post(
            OPENAI_API_URL,
            {
                model: 'gpt-4.1',
                messages,
            },
            {
                headers: {
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json',
                },
                timeout: 10000,
            }
        );
        console.log(response.data);
        return response.data;
    } catch (error: any) {
        console.log(error.response?.data || { message: error.message });
        throw error.response?.data || { message: error.message };
    }
}