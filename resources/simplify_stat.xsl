<?xml version="1.0" encoding="windows-1250"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
                xmlns:gml="http://www.opengis.net/gml/3.2"
                xmlns:xlink="http://www.w3.org/1999/xlink"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:ami="urn:cz:isvs:ruian:schemas:AdrMistoIntTypy:v1"
                xmlns:base="urn:cz:isvs:ruian:schemas:BaseTypy:v1"
                xmlns:coi="urn:cz:isvs:ruian:schemas:CastObceIntTypy:v1"
                xmlns:com="urn:cz:isvs:ruian:schemas:CommonTypy:v1"
                xmlns:kui="urn:cz:isvs:ruian:schemas:KatUzIntTypy:v1"
                xmlns:kri="urn:cz:isvs:ruian:schemas:KrajIntTypy:v1"
                xmlns:mci="urn:cz:isvs:ruian:schemas:MomcIntTypy:v1"
                xmlns:mpi="urn:cz:isvs:ruian:schemas:MopIntTypy:v1"
                xmlns:obi="urn:cz:isvs:ruian:schemas:ObecIntTypy:v1"
                xmlns:oki="urn:cz:isvs:ruian:schemas:OkresIntTypy:v1"
                xmlns:opi="urn:cz:isvs:ruian:schemas:OrpIntTypy:v1"
                xmlns:pai="urn:cz:isvs:ruian:schemas:ParcelaIntTypy:v1"
                xmlns:pui="urn:cz:isvs:ruian:schemas:PouIntTypy:v1"
                xmlns:rsi="urn:cz:isvs:ruian:schemas:RegSouIntiTypy:v1"
                xmlns:spi="urn:cz:isvs:ruian:schemas:SpravObvIntTypy:v1"
                xmlns:sti="urn:cz:isvs:ruian:schemas:StatIntTypy:v1"
                xmlns:soi="urn:cz:isvs:ruian:schemas:StavObjIntTypy:v1"
                xmlns:uli="urn:cz:isvs:ruian:schemas:UliceIntTypy:v1"
                xmlns:vci="urn:cz:isvs:ruian:schemas:VuscIntTypy:v1"
                xmlns:vf="urn:cz:isvs:ruian:schemas:VymennyFormatTypy:v1"
                xmlns:zji="urn:cz:isvs:ruian:schemas:ZsjIntTypy:v1"
                xmlns:voi="urn:cz:isvs:ruian:schemas:VOIntTypy:v1">

    <xsl:template match="vf:VymennyFormat">
        <!--  hlavicka zahozena-->
        <VymennyFormat>
            <xsl:apply-templates select="vf:Data"/>
        </VymennyFormat>
    </xsl:template>


    <xsl:template match="vf:Data">
        <Data>
            <xsl:apply-templates select="vf:Staty"/>

            <xsl:apply-templates select="vf:Kraje"/>

            <xsl:apply-templates select="vf:Okresy"/>

            <xsl:apply-templates select="vf:Obce"/>
        </Data>
    </xsl:template>

    <xsl:template match="vf:Staty">
        <Staty>
        <xsl:for-each select="vf:Stat">
            <Stat kod="{sti:Kod}">
                <Nazev>
                    <xsl:value-of select="sti:Nazev"/>
                </Nazev>
                <Geometrie>
                    <PosList>
                        <xsl:value-of select="sti:Geometrie//sti:GeneralizovaneHranice5//gml:MultiSurface//gml:surfaceMember//gml:Polygon//gml:exterior//gml:LinearRing//gml:posList"/>
                    </PosList>
                </Geometrie>
            </Stat>
        </xsl:for-each>
        </Staty>

    </xsl:template>


    <xsl:template match="vf:Kraje">
        <Kraje>
        <xsl:for-each select="vf:Kraj">
            <Kraj kod="{kri:Kod}">
                <Nazev>
                    <xsl:value-of select="kri:Nazev"/>
                </Nazev>
                <Geometrie>
                    <PosList>
                        <xsl:value-of select="kri:Geometrie//kri:GeneralizovaneHranice5//gml:MultiSurface//gml:surfaceMember//gml:Polygon//gml:exterior//gml:LinearRing//gml:posList"/>
                    </PosList>
                </Geometrie>
            </Kraj>
        </xsl:for-each>
        </Kraje>
    </xsl:template>


    <xsl:template match="vf:Okresy">
        <Okresy>
        <xsl:for-each select="vf:Okres">
            <Okres kod="{oki:Kod}"
                   kraj="{oki:Kraj//kri:Kod}">
                <Nazev>
                    <xsl:value-of select="oki:Nazev"/>
                </Nazev>
                <Geometrie>
                    <PosList>
                        <xsl:value-of select="oki:Geometrie//oki:GeneralizovaneHranice4//gml:MultiSurface//gml:surfaceMember//gml:Polygon//gml:exterior//gml:LinearRing//gml:posList"/>
                    </PosList>
                </Geometrie>
            </Okres>
        </xsl:for-each>
        </Okresy>
    </xsl:template>

    <xsl:template match="vf:Obce">
        <Obce>
        <xsl:for-each select="vf:Obec">
            <Obec kod="{obi:Kod}"
                  okres="{obi:Okres//oki:Kod}">
                <Nazev>
                    <xsl:value-of select="obi:Nazev"/>
                </Nazev>
                <Geometrie>
                    <PosList>
                        <xsl:value-of select="obi:Geometrie//obi:GeneralizovaneHranice3//gml:MultiSurface//gml:surfaceMember//gml:Polygon//gml:exterior//gml:LinearRing//gml:posList"/>
                    </PosList>
                </Geometrie>
            </Obec>
        </xsl:for-each>
        </Obce>
    </xsl:template>

</xsl:stylesheet>

