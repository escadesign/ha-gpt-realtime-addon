import os
class Settings:
    openai_api_key = os.getenv("OPENAI_API_KEY","")
    ha_url         = os.getenv("HA_URL","http://homeassistant.local:8123")
    ha_token       = os.getenv("HA_TOKEN","")
    language       = os.getenv("LANGUAGE","de")
    voice          = os.getenv("VOICE","alloy")
    sample_rate    = int(os.getenv("SAMPLE_RATE","24000"))
    input_device   = os.getenv("INPUT_DEVICE","auto")
    output_device  = os.getenv("OUTPUT_DEVICE","auto")
    require_auth   = os.getenv("REQUIRE_AUTH","true").lower()=="true"
    api_username   = os.getenv("API_USERNAME","admin")
    api_password   = os.getenv("API_PASSWORD","ha")
    mcp_enabled    = os.getenv("MCP_ENABLED","true").lower()=="true"
settings = Settings()
