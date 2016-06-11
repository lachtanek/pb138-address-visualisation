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
            <xsl:choose>
                <xsl:when test="vf:Ulice">
                    <!--Ulice-->
                    <xsl:apply-templates select="vf:Ulice"/>
                    <!--/Ulice-->
                </xsl:when>
                <xsl:otherwise>
                    <AdresniMista>
                        <xsl:variable name="soi"
                                      select="vf:AdresniMista//vf:AdresniMisto//ami:StavebniObjekt//soi:Kod"/>
                        <xsl:if test="vf:StavebniObjekty//vf:StavebniObjekt//soi:Kod=$soi">
                            <xsl:variable name="coi"
                                          select="vf:StavebniObjekty//vf:StavebniObjekt//soi:CastObce//coi:Kod"/>
                            <xsl:if test="vf:CastiObci//vf:CastObce//coi:Kod=$coi">
                                <xsl:variable name="obi" select="vf:CastiObci//vf:CastObce//coi:Obec//obi:Kod"/>

                                <xsl:attribute name="obec">
                                    <xsl:value-of select="$obi"/>
                                </xsl:attribute>
                            </xsl:if>
                        </xsl:if>
                        <PocetAdresnichMist>
                            <xsl:value-of select="count(vf:AdresniMista//vf:AdresniMisto)"/>
                        </PocetAdresnichMist>
                    </AdresniMista>
                </xsl:otherwise>
            </xsl:choose>
        </Data>
    </xsl:template>

    <xsl:template match="vf:Ulice">
        <xsl:for-each select="vf:Ulice">
            <Ulice kod="{uli:Kod}"
                   obec="{uli:Obec//obi:Kod}">
                <Nazev>
                    <xsl:value-of select="uli:Nazev"/>
                </Nazev>

                <xsl:variable name="kodUlice">
                    <xsl:value-of select="uli:Kod"/>
                </xsl:variable>

                <PocetAdresnichMist>
                    <xsl:value-of select="count(//vf:AdresniMisto[ami:Ulice[uli:Kod/text()=$kodUlice]])"/>
                </PocetAdresnichMist>

                
                    <xsl:apply-templates select="uli:Geometrie//uli:DefinicniCara//gml:MultiCurve"/>
                
            </Ulice>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="uli:Geometrie//uli:DefinicniCara//gml:MultiCurve">
      <Geometrie>
            <xsl:for-each select="gml:curveMember">
                <PosList>
                    <xsl:value-of select="gml:LineString//gml:posList"/>
                </PosList>
            </xsl:for-each>
      </Geometrie>      
    </xsl:template>
</xsl:stylesheet>