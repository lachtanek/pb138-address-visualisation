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
            <Staty>
                <xsl:apply-templates select="vf:Staty"/>
            </Staty>
            <RegionySoudrznosti>
                <xsl:apply-templates select="vf:RegionySoudrznosti"/>
            </RegionySoudrznosti>
            <Kraje>
                <xsl:apply-templates select="vf:Kraje"/>
            </Kraje>
            <Vusc>
                <xsl:apply-templates select="vf:Vusc"/>
            </Vusc>
            <Okresy>
                <xsl:apply-templates select="vf:Okresy"/>
            </Okresy>
            <Orp>
                <xsl:apply-templates select="vf:Orp"/>
            </Orp>
            <Pou>
                <xsl:apply-templates select="vf:Pou"/>
            </Pou>
            <Obce>
                <xsl:apply-templates select="vf:Obce"/>
            </Obce>
            <SpravniObvody>
                <xsl:apply-templates select="vf:SpravniObvody"/>
            </SpravniObvody>
            <Mop>
                <xsl:apply-templates select="vf:Mop"/>
            </Mop>
            <Momc>
                <xsl:apply-templates select="vf:Momc"/>
            </Momc>
            <!--CastiObci>
                <xsl:apply-templates select="vf:CastiObci"/>
            </CastiObci -->
            <KatastralniUzemi>
                <xsl:apply-templates select="vf:KatastralniUzemi"/>
            </KatastralniUzemi>
            <!--Zsj>
                <xsl:apply-templates select="vf:Zsj"/>
            </Zsj -->
        </Data>
    </xsl:template>

    <xsl:template match="vf:Staty">
        <xsl:for-each select="vf:Stat">
            <Stat kod="{sti:Kod}">
                <Nazev>
                    <xsl:value-of select="sti:Nazev"/>
                </Nazev>
            </Stat>
        </xsl:for-each>

    </xsl:template>

    <xsl:template match="vf:RegionySoudrznosti">
        <xsl:for-each select="vf:RegionSoudrznosti">
            <RegionSoudrznosti kod="{rsi:Kod}">
                <Nazev>
                    <xsl:value-of select="rsi:Nazev"/>
                </Nazev>
            </RegionSoudrznosti>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Kraje">
        <xsl:for-each select="vf:Kraj">
            <Kraj kod="{kri:Kod}">
                <Nazev>
                    <xsl:value-of select="kri:Nazev"/>
                </Nazev>
            </Kraj>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Vusc">
        <xsl:for-each select="vf:Vusc">
            <Vusc kod="{vci:Kod}">
                <Nazev>
                    <xsl:value-of select="vci:Nazev"/>
                </Nazev>
            </Vusc>
        </xsl:for-each>
    </xsl:template>


    <xsl:template match="vf:Okresy">
        <xsl:for-each select="vf:Okres">
            <Okres kod="{oki:Kod}">
                <Nazev>
                    <xsl:value-of select="oki:Nazev"/>
                </Nazev>
            </Okres>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Orp">
        <xsl:for-each select="vf:Orp">
            <Orp kod="{opi:Kod}"
                 spravniobec="{opi:SpravniObecKod}"
                 vusc="{opi:Vusc/vci:Kod}">
                <Nazev>
                    <xsl:value-of select="opi:Nazev"/>
                </Nazev>
            </Orp>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Pou">
        <xsl:for-each select="vf:Pou">
            <Pou kod="{pui:Kod}"
                 spravniobec="{pui:SpravniObecKod}"
                 opr="{pui:Orp/opi:Kod}">
                <Nazev>
                    <xsl:value-of select="pui:Nazev"/>
                </Nazev>
            </Pou>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Obce">
        <xsl:for-each select="vf:Obec">
            <Obec kod="{obi:Kod}"
                  okres="{obi:Okres//oki:Kod}"
                  pou="{obi:Pou//pui:Kod}">
                <Nazev>
                    <xsl:value-of select="obi:Nazev"/>
                </Nazev>
                <obi:StatusKod>
                    <xsl:value-of select="obi:StatusKod"/>
                </obi:StatusKod>
            </Obec>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:SpravniObvody">
        <xsl:for-each select="vf:SpravniObvod">
            <SpravniObvod kod="{spi:Kod}"
                          momc="{spi:SpravniMomcKod}"
                          obec="{spi:Obec/obi:Kod}">
                <Nazev>
                    <xsl:value-of select="spi:Nazev"/>
                </Nazev>
            </SpravniObvod>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Mop">
        <xsl:for-each select="vf:Mop">
            <Mop kod="{mpi:Kod}"
                 obec="{spi:Obec/obi:Kod}">
                <Nazev>
                    <xsl:value-of select="mpi:Nazev"/>
                </Nazev>
            </Mop>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Momc">
        <xsl:for-each select="vf:Momc">
            <Momc kod="{mci:Kod}"
                  mop="{mci:Mop/mpi:Kod}"
                  obec="{mci:Obec/obi:Kod}"
                  spravniobvod="{mci:SpravniObvod/spi:Kod}">
                <Nazev>
                    <xsl:value-of select="mci:Nazev"/>
                </Nazev>
            </Momc>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:CastiObci">
        <xsl:for-each select="vf:CastObce">
            <CastObce kod="{coi:Kod}"
                      obec="{coi:Obec//obi:Kod}">
                <Nazev>
                    <xsl:value-of select="coi:Nazev"/>
                </Nazev>
            </CastObce>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:KatastralniUzemi">
        <xsl:for-each select="vf:KatastralniUzemi">
            <KatastralniUzemi kod="{kui:Kod}"
                              obec="{kui:Obec//obi:Kod}">
                <Nazev>
                    <xsl:value-of select="kui:Nazev"/>
                </Nazev>
            </KatastralniUzemi>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Zsj">
        <xsl:for-each select="vf:Zsj">
            <Zsj kod="{zji:Kod}"
                 katastralniuzemi="{zji:KatastralniUzemi//kui:Kod}">
                <zji:Nazev>
                    <xsl:value-of select="zji:Nazev"/>
                </zji:Nazev>
                <zji:Vymera>
                    <xsl:value-of select="zji:Vymera"/>
                </zji:Vymera>
            </Zsj>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>

