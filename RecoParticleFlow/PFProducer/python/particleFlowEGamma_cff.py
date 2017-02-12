import FWCore.ParameterSet.Config as cms

#Geometry
# include used for track reconstruction 
# note that tracking is redone since we need updated hits and they 
# are not stored in the event!
from RecoParticleFlow.PFProducer.particleFlowEGamma_cfi import *
from RecoEgamma.EgammaPhotonProducers.gedPhotonSequence_cff import *
from RecoEgamma.EgammaElectronProducers.gedGsfElectronSequence_cff import *
from RecoEgamma.EgammaElectronProducers.pfBasedElectronIso_cff import *
from RecoEgamma.EgammaIsolationAlgos.particleBasedIsoProducer_cfi import particleBasedIsolation as _particleBasedIsolation
from RecoEgamma.EgammaIsolationAlgos.egmPhotonIsolationAOD_cff import egmPhotonIsolationAOD as _egmPhotonIsolationAOD
from RecoEgamma.EgammaIsolationAlgos.egmGedGsfElectronPFIsolation_cfi import egmGedGsfElectronPFNoPileUpIsolationMapBasedVeto as _egmElectronIsolationCITK
from RecoEgamma.EgammaIsolationAlgos.egmGedGsfElectronPFIsolation_cfi import egmGedGsfElectronPFPileUpIsolationMapBasedVeto as _egmElectronIsolationCITKPileUp


from CommonTools.ParticleFlow.pfNoPileUpIso_cff import pfPileUpIso, pfNoPileUpIso, pfNoPileUpIsoSequence
from CommonTools.ParticleFlow.ParticleSelectors.pfSortByType_cff import pfPileUpAllChargedParticles 
from RecoEgamma.EgammaIsolationAlgos.egmIsolationDefinitions_cff import pfNoPileUpCandidates
from RecoEgamma.EgammaIsolationAlgos.egmIsoConeDefinitions_cfi import IsoConeDefinitions  as IsoConeDefinitionsPhotonsTmp

particleBasedIsolationTmp = _particleBasedIsolation.clone()
particleBasedIsolationTmp.photonProducer =  cms.InputTag("gedPhotonsTmp")
particleBasedIsolationTmp.electronProducer = cms.InputTag("gedGsfElectronsTmp")
particleBasedIsolationTmp.pfCandidates = cms.InputTag("particleFlowTmp")
particleBasedIsolationTmp.valueMapPhoPFblockIso = cms.string("gedPhotonsTmp")
particleBasedIsolationTmp.valueMapElePFblockIso = cms.string("gedGsfElectronsTmp")

egmPhotonIsolationCITK = _egmPhotonIsolationAOD.clone()
egmElectronIsolationCITK = _egmElectronIsolationCITK.clone()
egmElectronIsolationPileUpCITK = _egmElectronIsolationCITKPileUp.clone()

for iPSet in IsoConeDefinitionsPhotonsTmp:
  iPSet.particleBasedIsolation = cms.InputTag("particleBasedIsolationTmp", "gedPhotonsTmp")

IsoConeDefinitionsElectronsTmp = IsoConeDefinitionsPhotonsTmp.clone()

for iPSet in IsoConeDefinitionsElectronsTmp:
  iPSet.particleBasedIsolation = cms.InputTag("particleBasedIsolationTmp", "gedGsfElectronsTmp")

#photon isolation sums
egmPhotonIsolationCITK.srcToIsolate = cms.InputTag("gedPhotonsTmp")
egmPhotonIsolationCITK.srcForIsolationCone = cms.InputTag("pfNoPileUpCandidates")
egmPhotonIsolationCITK.isolationConeDefinitions = IsoConeDefinitionsPhotonsTmp
#electrons isolation sums
egmElectronIsolationCITK.srcToIsolate = cms.InputTag("gedGsfElectronsTmp")
egmElectronIsolationCITK.srcForIsolationCone = cms.InputTag("pfNoPileUpCandidates")
egmElectronIsolationCITK.isolationConeDefinitions = IsoConeDefinitionsElectronsTmp
#electrons pileup isolation sum
egmElectronIsolationPileUpCITK.srcToIsolate = cms.InputTag("gedGsfElectronsTmp")
egmElectronIsolationPileUpCITK.srcForIsolationCone = cms.InputTag("pfPileUpAllChargedParticles")
egmElectronIsolationPileUpCITK.isolationConeDefinitions = IsoConeDefinitionsElectronsTmp

particleFlowEGammaFull = cms.Sequence(particleFlowEGamma*gedGsfElectronSequenceTmp*gedPhotonSequenceTmp)
particleFlowEGammaFinal = cms.Sequence(particleBasedIsolationTmp*pfNoPileUpIsoSequence*pfNoPileUpCandidates*pfPileUpAllChargedParticles*egmPhotonIsolationCITK*egmElectronIsolationCITK*gedPhotonSequence*gedElectronPFIsoSequence)
