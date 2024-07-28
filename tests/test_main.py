import logging
import pytest
from base64 import b64encode
from lxml import etree
from unittest.mock import patch, mock_open

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.testclient import TestClient
from httpx import AsyncClient
from pydantic import BaseModel

from app.main import app, AnnotationResponse, authenticate
from app.utils import convert_to_custom_xml

security = HTTPBasic()

USERNAME = "myUser123"
PASSWORD = "secretSecret"

def test_convert_to_custom_xml_success():
    # Sample XML input
    input_xml = '''<root>
                       <element>Text</element>
                   </root>'''

    # Expected XML output after transformation
    expected_output_xml = '''<element_transformed>Text</element_transformed>'''

    # Mock XSLT content
    xslt_content = '''<xsl:stylesheet version="1.0"
                        xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
                        <xsl:template match="/root">
                            <xsl:apply-templates select="element"/>
                        </xsl:template>
                        <xsl:template match="element">
                            <element_transformed>
                                <xsl:value-of select="."/>
                            </element_transformed>
                        </xsl:template>
                      </xsl:stylesheet>'''

    with patch("builtins.open", mock_open(read_data=xslt_content)):
        with patch("app.utils.etree.parse") as mock_parse:
            mock_parse.side_effect = lambda _: etree.fromstring(xslt_content)
            result = convert_to_custom_xml(input_xml)
            assert result.strip() == expected_output_xml.strip()

def test_convert_to_custom_xml_invalid_xml():
    # Invalid XML input
    invalid_input_xml = '''<root>
                              <element>Text
                          </root>'''  # Missing closing tag for <element>

    with pytest.raises(etree.XMLSyntaxError):
        convert_to_custom_xml(invalid_input_xml)

@pytest.mark.asyncio
async def test_export():
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        username = "myUser123"
        password = "secretSecret"
        auth_header = b64encode(f"{username}:{password}".encode()).decode()

        response = await test_client.post(
            "/export/3398820/1192052",
            headers={"Authorization": f"Basic {auth_header}"}
        )
        assert response.status_code == 200
        assert response.json()["success"] is True

@app.get("/secure-endpoint")
def secure_endpoint(credentials: HTTPBasicCredentials = Depends(authenticate)):
    return AnnotationResponse(success=True)


client = TestClient(app)
def test_authenticate_success():
    response = client.get(
        "/secure-endpoint",
        auth=(USERNAME, PASSWORD)
    )
    assert response.status_code == 200
    assert response.json() == {"success": True}

def test_authenticate_failure():
    response = client.get(
        "/secure-endpoint",
        auth=("wrongUser", "wrongPassword")
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
