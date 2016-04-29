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
        <vf:VymennyFormat>
            <xsl:apply-templates select="vf:Data"/>
        </vf:VymennyFormat>
    </xsl:template>


    <xsl:template match="vf:Data">
        <vf:Staty>
            <xsl:apply-templates select="vf:Staty"/>
        </vf:Staty>
        <vf:RegionySoudrznosti>
            <xsl:apply-templates select="vf:RegionySoudrznosti"/>
        </vf:RegionySoudrznosti>
        <vf:Kraje>
            <xsl:apply-templates select="vf:Kraje"/>
        </vf:Kraje>
        <vf:Vusc>
            <xsl:apply-templates select="vf:Vusc"/>
        </vf:Vusc>
        <vf:Okresy>
            <xsl:apply-templates select="vf:Okresy"/>
        </vf:Okresy>
        <vf:Orp>
            <xsl:apply-templates select="vf:Orp"/>
        </vf:Orp>
        <vf:Pou>
            <xsl:apply-templates select="vf:Pou"/>
        </vf:Pou>
        <vf:Obce>
            <xsl:apply-templates select="vf:Obce"/>
        </vf:Obce>
        <vf:SpravniObvody>
            <xsl:apply-templates select="vf:SpravniObvody"/>
        </vf:SpravniObvody>
        <vf:Mop>
            <xsl:apply-templates select="vf:Mop"/>
        </vf:Mop>
        <vf:Momc>
            <xsl:apply-templates select="vf:Momc"/>
        </vf:Momc>
        <vf:CastiObci>
            <xsl:apply-templates select="vf:CastiObci"/>
        </vf:CastiObci>
        <vf:KatastralniUzemi>
            <xsl:apply-templates select="vf:KatastralniUzemi"/>
        </vf:KatastralniUzemi>
        <vf:Zsj>
            <xsl:apply-templates select="vf:Zsj"/>
        </vf:Zsj>
    </xsl:template>

    <xsl:template match="vf:Staty">
        <xsl:for-each select="vf:Stat">
            <vf:Stat>
                <sti:Kod>
                    <xsl:value-of select="sti:Kod"/>
                </sti:Kod>
                <sti:Nazev>
                    <xsl:value-of select="sti:Nazev"/>
                </sti:Nazev>
            </vf:Stat>
        </xsl:for-each>

    </xsl:template>

    <xsl:template match="vf:RegionySoudrznosti">
        <xsl:for-each select="vf:RegionSoudrznosti">
            <vf:RegionSoudrznosti>
                <rsi:Kod>
                    <xsl:value-of select="rsi:Kod"/>
                </rsi:Kod>
                <rsi:Nazev>
                    <xsl:value-of select="rsi:Nazev"/>
                </rsi:Nazev>
            </vf:RegionSoudrznosti>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Kraje">
        <xsl:for-each select="vf:Kraj">
            <vf:Kraj>
                <kri:Kod>
                    <xsl:value-of select="kri:Kod"/>
                </kri:Kod>
                <kri:Nazev>
                    <xsl:value-of select="kri:Nazev"/>
                </kri:Nazev>
            </vf:Kraj>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Vusc">
        <xsl:for-each select="vf:Vusc">
            <vf:Vusc>
                <vci:Kod>
                    <xsl:value-of select="vci:Kod"/>
                </vci:Kod>
                <kri:Nazev>
                    <xsl:value-of select="kri:Nazev"/>
                </kri:Nazev>
            </vf:Vusc>
        </xsl:for-each>
    </xsl:template>


    <xsl:template match="vf:Okresy">
        <xsl:for-each select="vf:Okres">
            <vf:Okres>
                <oki:Kod>
                    <xsl:value-of select="oki:Kod"/>
                </oki:Kod>
                <oki:Nazev>
                    <xsl:value-of select="oki:Nazev"/>
                </oki:Nazev>
            </vf:Okres>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Orp">
        <xsl:for-each select="vf:Orp">
            <vf:Orp>
                <opi:Kod>
                    <xsl:value-of select="opi:Kod"/>
                </opi:Kod>
                <opi:Nazev>
                    <xsl:value-of select="opi:Nazev"/>
                </opi:Nazev>
                <opi:SpravniObecKod>
                    <xsl:value-of select="opi:SpravniObecKod"/>
                </opi:SpravniObecKod>
                <opi:Vusc>
                    <vci:Kod>
                        <xsl:value-of select="opi:Vusc/vci:Kod"/>
                    </vci:Kod>
                </opi:Vusc>
            </vf:Orp>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Pou">
        <xsl:for-each select="vf:Pou">
            <vf:Pou>
                <pui:Kod>
                    <xsl:value-of select="pui:Kod"/>
                </pui:Kod>
                <pui:Nazev>
                    <xsl:value-of select="pui:Nazev"/>
                </pui:Nazev>
                <pui:SpravniObecKod>
                    <xsl:value-of select="pui:SpravniObecKod"/>
                </pui:SpravniObecKod>
                <pui:Orp>
                    <opi:Kod>
                        <xsl:value-of select="pui:Orp/opi:Kod"/>
                    </opi:Kod>
                </pui:Orp>
            </vf:Pou>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Obce">
        <xsl:for-each select="vf:Obec">
            <vf:Obec>
                <obi:Kod>
                    <xsl:value-of select="obi:Kod"/>
                </obi:Kod>
                <obi:Nazev>
                    <xsl:value-of select="obi:Nazev"/>
                </obi:Nazev>
                <obi:StatusKod>
                    <xsl:value-of select="obi:StatusKod"/>
                </obi:StatusKod>
                <obi:Okres>
                    <oki:Kod>
                        <xsl:value-of select="obi:Okres/oki:Kod"/>
                    </oki:Kod>
                </obi:Okres>
                <obi:Pou>
                    <pui:Kod>
                        <xsl:value-of select="obi:Pou/pui:Kod"/>
                    </pui:Kod>
                </obi:Pou>
            </vf:Obec>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:SpravniObvody">
        <xsl:for-each select="vf:SpravniObvod">
            <vf:SpravniObvod>
                <spi:Kod>
                    <xsl:value-of select="spi:Kod"/>
                </spi:Kod>
                <spi:Nazev>
                    <xsl:value-of select="spi:Nazev"/>
                </spi:Nazev>
                <spi:SpravniMomcKod>
                    <xsl:value-of select="spi:SpravniMomcKod"/>
                </spi:SpravniMomcKod>
                <spi:Obec>
                    <obi:Kod>
                        <xsl:value-of select="spi:Obec/obi:Kod"/>
                    </obi:Kod>
                </spi:Obec>
            </vf:SpravniObvod>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Mop">
        <xsl:for-each select="vf:Mop">
            <vf:Mop>
                <mpi:Kod>
                    <xsl:value-of select="mpi:Kod"/>
                </mpi:Kod>
                <mpi:Nazev>
                    <xsl:value-of select="mpi:Nazev"/>
                </mpi:Nazev>
                <mpi:Obec>
                    <obi:Kod>
                        <xsl:value-of select="mpi:Obec/obi:Kod"/>
                    </obi:Kod>
                </mpi:Obec>
            </vf:Mop>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Momc">
        <xsl:for-each select="vf:Momc">
            <vf:Momc>
                <mci:Kod>
                    <xsl:value-of select="mci:Kod"/>
                </mci:Kod>
                <mci:Nazev>
                    <xsl:value-of select="mci:Nazev"/>
                </mci:Nazev>
                <mci:Mop>
                    <mpi:Kod>
                        <xsl:value-of select="mci:Mop/mpi:Kod"/>
                    </mpi:Kod>
                </mci:Mop>
                <mci:Obec>
                    <obi:Kod>
                        <xsl:value-of select="mci:Obec/obi:Kod"/>
                    </obi:Kod>
                </mci:Obec>
                <mci:SpravniObvod>
                    <spi:Kod>
                        <xsl:value-of select="mci:SpravniObvod/spi:Kod"/>
                    </spi:Kod>
                </mci:SpravniObvod>
            </vf:Momc>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:CastiObci">
        <xsl:for-each select="vf:CastObce">
            <vf:CastObce>
                <coi:Kod>
                    <xsl:value-of select="coi:Kod"/>
                </coi:Kod>
                <coi:Nazev>
                    <xsl:value-of select="coi:Nazev"/>
                </coi:Nazev>
                <coi:Obec>
                    <obi:Kod>
                        <xsl:value-of select="coi:Obec/obi:Kod"/>
                    </obi:Kod>
                </coi:Obec>
            </vf:CastObce>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:KatastralniUzemi">
        <xsl:for-each select="vf:KatastralniUzemi">
            <vf:KatastralniUzemi>
                <kui:Kod>
                    <xsl:value-of select="kui:Kod"/>
                </kui:Kod>
                <kui:Nazev>
                    <xsl:value-of select="kui:Nazev"/>
                </kui:Nazev>
                <kui:Obec>
                    <obi:Kod>
                        <xsl:value-of select="kui:Obec/obi:Kod"/>
                    </obi:Kod>
                </kui:Obec>
            </vf:KatastralniUzemi>
        </xsl:for-each>
    </xsl:template>
    <xsl:template match="vf:Zsj">
        <xsl:for-each select="vf:Zsj">
            <vf:Zsj>
                <zji:Kod>
                    <xsl:value-of select="zji:Kod"/>
                </zji:Kod>
                <zji:Nazev>
                    <xsl:value-of select="zji:Nazev"/>
                </zji:Nazev>
                <zji:KatastralniUzemi>
                    <kui:Kod>
                        <xsl:value-of select="zji:KatastralniUzemi/kui:Kod"/>
                    </kui:Kod>
                </zji:KatastralniUzemi>
                <zji:Vymera>
                    <xsl:value-of select="zji:Vymera"/>
                </zji:Vymera>
            </vf:Zsj>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>

