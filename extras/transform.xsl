<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="text"/>

	<xsl:template match="property-list/object/object">
            <xsl:for-each select="object">
               <xsl:text>['</xsl:text>
               <xsl:value-of select="string"/>
               <xsl:text>', '</xsl:text>
               <xsl:value-of select="@name"/>
               <xsl:text>', '', [</xsl:text>
                  <xsl:for-each select="array/string">
                     <xsl:text>'</xsl:text>
                     <xsl:value-of select="."/>
                     <xsl:text>'</xsl:text>
                     <xsl:if test="not(position() = last())">
                        <xsl:text>, </xsl:text>
                     </xsl:if>
                  </xsl:for-each>
               <xsl:text>] ],&#xA;</xsl:text>
            </xsl:for-each>
	</xsl:template>
</xsl:stylesheet>
