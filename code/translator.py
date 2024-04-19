import requests

STE_LLAMA2_EIC = "https://rd1kgw40ukamey40.us-east-1.aws.endpoints.huggingface.cloud"
LLAMA2_7B_MINI_STE_BJI = "https://po31as4mtpskbg57.us-east-1.aws.endpoints.huggingface.cloud"
API_URL = LLAMA2_7B_MINI_STE_BJI
API_TOKEN = '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'  # TODO: this is a security risk
headers = {
	"Accept" : "application/json",
	"Authorization": f"Bearer {API_TOKEN}",
	"Content-Type": "application/json" 
}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def translate(in_text):
    output = query({
	    "inputs": in_text,
	    "parameters": {}
    })
    return output[0]['generated_text']


if __name__ == '__main__':
    print(translate("Please rewrite this sentence."))
