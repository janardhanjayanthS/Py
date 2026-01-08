import requests

# Base URL for MedlinePlus Connect
url = "https://connect.medlineplus.gov/service"


async def access_medical_api(disease_code: str) -> str:
    params = {
        "mainSearchCriteria.v.cs": "2.16.840.1.113883.6.90",  # OID for ICD-10-CM
        "mainSearchCriteria.v.c": disease_code,  # Code for Diabetes
        "knowledgeResponseType": "application/json",  # Request JSON format
    }

    try:
        response = await requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            entry = data.get("feed", {}).get("entry", [{}])[0]
            summary = entry.get("summary", {}).get("_value", "No Summary Found")
            return summary
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")
