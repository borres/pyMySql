<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" encoding="utf-8"/>
<!--
Producing strait json
either from a mysqldump of one table to xml
or from mysql extract to xmlfile  with sql

Limitation:
Replace " with /" in values,
as from:
http://stackoverflow.com/questions/9370633/xslt-replacing-double-quotes-with-escape-sequence

no other cleaning or escaping

alternativ stylesheet at:
http://code.google.com/p/xml2json-xslt/


-->

<xsl:template match="/">
{"list":[<xsl:apply-templates select="//row"/>]}
</xsl:template>

<xsl:template match="row">
{<xsl:apply-templates select="field"/>
}
<xsl:if test="position() &lt; last()">,</xsl:if>
</xsl:template>

<xsl:template match="//row/field">
"<xsl:value-of select="@name"/>":"<xsl:call-template name="escapeQuote"/>"<xsl:if test="position() &lt; last()">,</xsl:if>
</xsl:template>

<!-- as from 
http://stackoverflow.com/questions/9370633/xslt-replacing-double-quotes-with-escape-sequence
-->
<xsl:template name="escapeQuote">
  <xsl:param name="pText" select="."/>

  <xsl:if test="string-length($pText) >0">
   <xsl:value-of select="substring-before(concat($pText, '&quot;'), '&quot;')"/>

   <xsl:if test="contains($pText, '&quot;')">
  <xsl:text>\"</xsl:text>

	<xsl:call-template name="escapeQuote">
	  <xsl:with-param name="pText" select="substring-after($pText, '&quot;')"/>
	</xsl:call-template>
   </xsl:if>
  </xsl:if>
</xsl:template>

</xsl:stylesheet>
