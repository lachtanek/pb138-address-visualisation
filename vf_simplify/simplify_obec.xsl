<?xml version="1.0" encoding="windows-1250"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
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
            <Ulice>
                <xsl:apply-templates select="vf:Ulice"/>
            </Ulice>
        </Data>
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

                <pocetAdresnichMist>
                    <xsl:value-of select="count(//vf:AdresniMisto[ami:Ulice[uli:Kod/text()=$kodUlice]])" />
                </pocetAdresnichMist>
            </Ulice>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:Parcely">
        <xsl:for-each select="vf:Parcela">
            <Parcela pai:Id="{pai:Id}" kui:Kod="{pai:KatastralniUzemi//kui:Kod}">
            </Parcela>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:StavebniObjekty">
        <xsl:for-each select="vf:StavebniObjekt">
            <StavebniObjekt soi:Kod="{soi:Kod}"
                            com:CisloDomovni="{soi:CislaDomovni//com:CisloDomovni}"
                            pai:Id="{soi:IdentifikacniParcela//pai:Id}"
                            coi:Kod="{soi:CastObce//coi:Kod}">
                <TypStavebnihoObjektuKod>
                    <xsl:value-of select="soi:TypStavebnihoObjektuKod"/>
                </TypStavebnihoObjektuKod>
                <ZpusobVyuzitiKod>
                    <xsl:value-of select="soi:ZpusobVyuzitiKod"/>
                </ZpusobVyuzitiKod>
                <PocetBytu>
                    <xsl:value-of select="soi:PocetBytu"/>
                </PocetBytu>
                <PocetPodlazi>
                    <xsl:value-of select="soi:PocetPodlazi"/>
                </PocetPodlazi>
                <PodlahovaPlocha>
                    <xsl:value-of select="soi:PodlahovaPlocha"/>
                </PodlahovaPlocha>
                <PripojeniKanalizaceKod>
                    <xsl:value-of select="soi:PripojeniKanalizaceKod"/>
                </PripojeniKanalizaceKod>
                <PripojeniPlynKod>
                    <xsl:value-of select="soi:PripojeniPlynKod"/>
                </PripojeniPlynKod>
                <PripojeniVodovodKod>
                    <xsl:value-of select="soi:PripojeniVodovodKod"/>
                </PripojeniVodovodKod>
                <VybaveniVytahemKod>
                    <xsl:value-of select="soi:VybaveniVytahemKod"/>
                </VybaveniVytahemKod>
                <ZpusobVytapeniKod>
                    <xsl:value-of select="soi:ZpusobVytapeniKod"/>
                </ZpusobVytapeniKod>
                <pocetAdresnichMist>

                </pocetAdresnichMist>
            </StavebniObjekt>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="vf:AdresniMista">
        <xsl:for-each select="vf:AdresniMisto">
            <AdresniMisto ami:Kod="{ami:Kod}"
                          soi:Kod="{ami:StavebniObjekt//soi:Kod}"
                          uli:Kod="{ami:Ulice//uli:Kod}">
                <CisloDomovni>
                    <xsl:value-of select="ami:CisloDomovni"/>
                </CisloDomovni>
                <Psc>
                    <xsl:value-of select="ami:Psc"/>
                </Psc>
            </AdresniMisto>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>