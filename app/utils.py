import json
import logging
import shlex

from lxml import etree

logger = logging.getLogger(__name__)


def convert_to_custom_xml(data):
    try:
        # Load the input XML data
        xml_data = etree.fromstring(data.encode("utf-8"))

        # Load the XSLT stylesheet
        xslt_doc = etree.parse("app/schema/transform.xslt")
        xslt_transformer = etree.XSLT(xslt_doc)

        # Apply the XSLT transformation
        transformed_doc = xslt_transformer(xml_data)

        # Convert the transformed XML to a string
        output_xml = etree.tostring(
            transformed_doc, pretty_print=True, encoding="unicode"
        )

        return output_xml
    except etree.XMLSyntaxError as e:
        logger.error("XML parsing error: %s", e)
        raise
    except etree.XSLTApplyError as e:
        logger.error("XSLT transformation error: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        raise


def log_request_as_curl(request):
    """
    Generates a cURL command equivalent to the HTTP request.
    """
    method = request.method
    url = request.url
    headers = request.headers

    if hasattr(request, "body"):
        body = request.body.decode() if request.body else ""
    else:
        body = ""

    curl_command = f"curl -X {method} {shlex.quote(str(url))}"

    # Add headers
    for key, value in headers.items():
        curl_command += f" -H {shlex.quote(f'{key}: {value}')}"

    # Add body
    if body:
        try:
            json_body = json.loads(body)
            formatted_body = json.dumps(json_body)
        except ValueError:
            formatted_body = body
        curl_command += f" -d {shlex.quote(formatted_body)}"

    return curl_command
