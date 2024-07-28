<?xml version="1.0" encoding="utf-8"?>
<xsl:transform version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <xsl:apply-templates select="export/results/annotation/content" />
    </xsl:template>
    <xsl:template match="export/results/annotation/content">
        <InvoiceRegisters>
            <Invoices>
                <Payable>
                    <InvoiceNumber>
                        <xsl:value-of select="section[@schema_id='invoice_info_section']/datapoint[@schema_id='document_id']" />
                    </InvoiceNumber>
                    <InvoiceDate>
                        <xsl:value-of select="section[@schema_id='invoice_info_section']/datapoint[@schema_id='date_issue']" />
                    </InvoiceDate>
                    <DueDate>
                        <xsl:value-of select="section[@schema_id='invoice_info_section']/datapoint[@schema_id='date_due']" />
                    </DueDate>
                    <TotalAmount>
                        <xsl:value-of select="section[@schema_id='amounts_section']/datapoint[@schema_id='amount_total']" />
                    </TotalAmount>
                    <Notes />
                    <Iban>
                        <xsl:value-of select="section[@schema_id='payment_info_section']/datapoint[@schema_id='iban']" />
                    </Iban>
                    <Amount>
                        <xsl:value-of select="section[@schema_id='amounts_section']/datapoint[@schema_id='amount_total_tax']" />
                    </Amount>
                    <Currency>
                        <xsl:value-of select="section[@schema_id='amounts_section']/datapoint[@schema_id='currency']" />
                    </Currency>
                    <Vendor>
                        <xsl:value-of select="section[@schema_id='vendor_section']/datapoint[@schema_id='sender_name']" />
                    </Vendor>
                    <VendorAddress>
                        <xsl:value-of select="section[@schema_id='vendor_section']/datapoint[@schema_id='sender_address']" />
                    </VendorAddress>
                    <Details>
                        <xsl:for-each select="section[@schema_id='line_items_section']/multivalue[@schema_id='line_items']/tuple[@schema_id='line_item']">
                            <Detail>
                                <Amount>
                                    <xsl:value-of select="datapoint[@schema_id='item_amount_total']" />
                                </Amount>
                                <AccountId />
                                <Quantity>
                                    <xsl:value-of select="datapoint[@schema_id='item_quantity']" />
                                </Quantity>
                                <Notes>
                                    <xsl:value-of select="datapoint[@schema_id='item_description']" />
                                </Notes>
                            </Detail>
                        </xsl:for-each>
                    </Details>
                </Payable>
            </Invoices>
        </InvoiceRegisters>
    </xsl:template>
</xsl:transform>