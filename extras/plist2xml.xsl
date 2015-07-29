<?xml version="1.0" encoding="utf-8"?>

<!-- Stylesheet for converting between plist and an intermediate format -->
<!-- Copyright 2006 Theo Hultberg, all rights reserved -->
<!-- Originally: http://blog.iconara.net/2006/12/13/xsl-and-plists -->
<!-- With fixes from here: -->
<!-- https://gist.github.com/elmimmo/2851115 -->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

	<xsl:output method="xml"
	            indent="yes"
	            encoding="UTF-8"
	            standalone="yes"
	/>

	<xsl:template match="/">
		<property-list>
			<xsl:apply-templates/>
		</property-list>
	</xsl:template>

	<xsl:template match="key"/>

	<xsl:template match="key" mode="dict"/>

	<xsl:template match="dict">
		<object>
			<xsl:apply-templates mode="dict"/>
		</object>
	</xsl:template>

	<xsl:template match="dict" mode="dict">
		<xsl:variable name="name">
			<xsl:value-of select="preceding-sibling::key[1]/text()"/>
		</xsl:variable>
		<object name="{$name}">
			<xsl:apply-templates mode="dict"/>
		</object>
	</xsl:template>

	<xsl:template match="true|false">
		<xsl:text>true</xsl:text>
	</xsl:template>

	<xsl:template match="true|false" mode="dict">
		<xsl:variable name="name">
			<xsl:value-of select="preceding-sibling::key[1]/text()"/>
		</xsl:variable>
		<xsl:variable name="type">
			<xsl:value-of select="'bool'"/>
		</xsl:variable>

		<property name="{$name}" type="{$type}">
			<xsl:value-of select="local-name()"/>
		</property>

	</xsl:template>

	<xsl:template match="string|integer|real|date">
		<xsl:element name="{local-name()}">
			<xsl:value-of select="text()"/>
		</xsl:element>
	</xsl:template>

	<xsl:template match="string|integer|real|date" mode="dict">
		<xsl:variable name="name">
			<xsl:value-of select="preceding-sibling::key[1]/text()"/>
		</xsl:variable>
		<xsl:variable name="type">
			<xsl:value-of select="local-name()"/>
		</xsl:variable>

		<xsl:element name="{$type}">
			<xsl:attribute name="name">
				<xsl:value-of select="$name"/>
			</xsl:attribute>

			<xsl:value-of select="text()"/>
		</xsl:element>
	</xsl:template>

	<xsl:template match="array">
		<array>
			<xsl:apply-templates/>
		</array>
	</xsl:template>

	<xsl:template match="array" mode="dict">
		<xsl:variable name="name">
			<xsl:value-of select="preceding-sibling::key[1]/text()"/>
		</xsl:variable>

		<array name="{$name}">
			<xsl:apply-templates/>
		</array>
	</xsl:template>

</xsl:stylesheet>
