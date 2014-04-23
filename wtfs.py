#!/usr/bin/env python
#
# wtfs.py will mount a filesystem at a directory and produce some
#         files with spam messages inside
#
# The word list used to generate the filenames and the spam messages
# are included directly in this file
#
# As this involves mounting and unmounting filesystems, you will need to be
# root (or know how to use fusermount and be a member of the fuse group)


import fuse
import sys
import stat
import hashlib
import random
import time


DIR_ENTRY_RANGE = (8, 20)
REGEN_CONTENTS_TIMEOUT = 3 # seconds


def get_index(path):
    return path.__hash__() % len(SPAMS)


def get_spam(path):
    index = get_index(path)
    spam = SPAMS[index].decode('rot13')
    # First two lines are always "Today's Spam:" and a newline
    # so trim those and the final trailing newline
    spam_text = "\n".join(spam.split('\n')[2:])
    return spam_text


def get_word(seed):
    hash_int = hashlib.md5(seed).digest().__hash__()
    index = hash_int % len(WORDS)
    return WORDS[index]


class WTFS(fuse.Fuse):
    def __init__(self, *args, **kwargs):
        fuse.fuse_python_api = (0, 2)
        fuse.Fuse.__init__(self, *args, **kwargs)
        self.read_only = True
        self.__set_dir_contents()

    def __set_dir_contents(self):
        now = int(time.time())
        self.last_readdir_time = now
        self.dir_contents = [fuse.Direntry(get_word(str(now + i)))
                             for i in range(random.randint(*DIR_ENTRY_RANGE))]

    def readdir(self, path, offset):
        for dir_entry in self.dir_contents:
            now = int(time.time())
            if self.last_readdir_time < now - REGEN_CONTENTS_TIMEOUT:
                self.__set_dir_contents()
            self.last_readdir_time = now
            yield dir_entry

    def getattr(self, path):
        st = fuse.Stat()
        if path == '/':
            st.st_mode = stat.S_IFDIR | 0555
            st.st_nlink = len(self.dir_contents)
        else:
            st.st_mode = stat.S_IFREG | 0444
            st.st_nlink = 1
            st.st_ino = get_index(path)
            st.st_uid = 0
            st.st_gid = 0
            st.st_size = len(bytes(get_spam(path)))
        return st

    def utime(self, path, times):
        return 0

    def open(self, path, flags):
        return 0

    def read(self, path, length, offset):
        return bytes(get_spam(path)[offset:offset+length])


def main():
    wtfs = WTFS()
    if len(sys.argv) != 2:
        print "usage: {} mountpoint".format(sys.argv[0])
        sys.exit(1)
    wtfs.parse(['-o', 'fsname=wtfs', sys.argv[1]])
    wtfs.main()


WORDS = """
a
aardvark
abaci
aback
abacus
abacuses
abandon
abandoned
abandoning
abandonment
abandons
abate
abated
abates
abating
abbey
abbeys
abbot
abbots
abbreviate
abbreviated
abbreviates
abbreviating
abbreviation
abbreviations
abdicate
abdicated
abdicates
abdicating
abdication
abdications
abdomen
abdomens
abdominal
abduct
abducted
abducting
abducts
aberration
aberrations
abet
abets
abetted
abetting
abhor
abhorred
abhorrence
abhorrent
abhorring
abhors
abide
abided
abides
abiding
abilities
ability
abject
ablaze
able
abler
ablest
ably
abnormal
abnormalities
abnormality
abnormally
aboard
abode
abodes
abolish
abolished
abolishes
abolishing
abolition
abominable
abomination
aboriginal
aborigine
aborigines
abort
aborted
aborting
abortion
abortions
abortive
aborts
abound
abounded
abounding
abounds
about
above
aboveboard
abrasive
abrasives
abreast
abridge
abridged
abridges
abridging
abroad
abrupt
abrupter
abruptest
abruptly
abscess
abscessed
abscesses
abscessing
abscond
absconded
absconding
absconds
absence
absences
absent
absented
absentee
absentees
absenting
absents
absolute
absolutely
absolutes
absolutest
absolve
absolved
absolves
absolving
absorb
absorbed
absorbent
absorbents
absorbing
absorbs
absorption
abstain
abstained
abstaining
abstains
abstention
abstentions
abstinence
abstract
abstracted
abstracting
abstraction
abstractions
abstracts
abstruse
absurd
absurder
absurdest
absurdities
absurdity
absurdly
abundance
abundances
abundant
abundantly
abuse
abused
abuser
abusers
abuses
abusing
abusive
abysmal
abyss
abysses
academic
academically
academics
academies
academy
accede
acceded
accedes
acceding
accelerate
accelerated
accelerates
accelerating
acceleration
accelerations
accelerator
accelerators
accent
accented
accenting
accents
accentuate
accentuated
accentuates
accentuating
accept
acceptability
acceptable
acceptably
acceptance
acceptances
accepted
accepting
accepts
access
accessed
accesses
accessibility
accessible
accessing
accessories
accessory
accident
accidental
accidentally
accidentals
accidents
acclaim
acclaimed
acclaiming
acclaims
acclimate
acclimated
acclimates
acclimating
acclimatize
acclimatized
acclimatizes
acclimatizing
accolade
accolades
accommodate
accommodated
accommodates
accommodating
accommodation
accommodations
accompanied
accompanies
accompaniment
accompaniments
accompanist
accompanists
accompany
accompanying
accomplice
accomplices
accomplish
accomplished
accomplishes
accomplishing
accomplishment
accomplishments
accord
accordance
accorded
according
accordingly
accordion
accordions
accords
accost
accosted
accosting
accosts
account
accountability
accountable
accountancy
accountant
accountants
accounted
accounting
accounts
accredit
accredited
accrediting
accredits
accrue
accrued
accrues
accruing
accumulate
accumulated
accumulates
accumulating
accumulation
accumulations
accuracy
accurate
accurately
accusation
accusations
accuse
accused
accuser
accusers
accuses
accusing
accustom
accustomed
accustoming
accustoms
ace
aced
aces
ache
ached
aches
achievable
achieve
achieved
achievement
achievements
achieves
achieving
aching
acid
acidity
acids
acing
acknowledge
acknowledged
acknowledgement
acknowledgements
acknowledges
acknowledging
acknowledgment
acknowledgments
acne
acorn
acorns
acoustic
acoustics
acquaint
acquaintance
acquaintances
acquainted
acquainting
acquaints
acquiesce
acquiesced
acquiescence
acquiesces
acquiescing
acquire
acquired
acquires
acquiring
acquisition
acquisitions
acquit
acquits
acquittal
acquittals
acquitted
acquitting
acre
acreage
acreages
acres
acrid
acrider
acridest
acrimonious
acrimony
acrobat
acrobatic
acrobatics
acrobats
acronym
acronyms
across
acrylic
acrylics
act
acted
acting
action
actions
activate
activated
activates
activating
active
actively
actives
activist
activists
activities
activity
actor
actors
actress
actresses
acts
actual
actualities
actuality
actually
actuary
acumen
acupuncture
acute
acutely
acuter
acutes
acutest
ad
adage
adages
adamant
adapt
adaptable
adaptation
adaptations
adapted
adapter
adapting
adaptive
adaptor
adapts
add
added
addendum
addict
addicted
addicting
addiction
addictions
addictive
addicts
adding
addition
additional
additionally
additions
additive
additives
address
addressed
addressee
addressees
addresses
addressing
adds
adept
adepts
adequate
adequately
adhere
adhered
adherence
adherent
adherents
adheres
adhering
adhesion
adhesive
adhesives
adjacent
adjective
adjectives
adjoin
adjoined
adjoining
adjoins
adjourn
adjourned
adjourning
adjournment
adjournments
adjourns
adjunct
adjuncts
adjust
adjustable
adjusted
adjusting
adjustment
adjustments
adjusts
administer
administered
administering
administers
administration
administrations
administrative
administrator
administrators
admirable
admirably
admiral
admirals
admiration
admire
admired
admirer
admirers
admires
admiring
admissible
admission
admissions
admit
admits
admittance
admitted
admittedly
admitting
admonish
admonished
admonishes
admonishing
admonition
admonitions
ado
adobe
adobes
adolescence
adolescences
adolescent
adolescents
adopt
adopted
adopting
adoption
adoptions
adopts
adorable
adoration
adore
adored
adores
adoring
adorn
adorned
adorning
adornment
adornments
adorns
adrift
adroit
adroitly
ads
adulation
adult
adulterate
adulterated
adulterates
adulterating
adulteration
adulteries
adultery
adulthood
adults
advance
advanced
advancement
advancements
advances
advancing
advantage
advantaged
advantageous
advantages
advantaging
advent
adventure
adventured
adventurer
adventurers
adventures
adventuring
adventurous
adverb
adverbial
adverbials
adverbs
adversaries
adversary
adverse
adversely
adverser
adversest
adversities
adversity
advert
advertise
advertised
advertisement
advertisements
advertiser
advertisers
advertises
advertising
adverts
advice
advisable
advise
advised
adviser
advisers
advises
advising
advisor
advisories
advisors
advisory
advocate
advocated
advocates
advocating
aeon
aeons
aerial
aerials
aerodynamic
aerodynamics
aerosol
aerosols
aerospace
aesthetic
aesthetically
afar
affable
affably
affair
affairs
affect
affectation
affectations
affected
affecting
affection
affectionate
affectionately
affections
affects
affidavit
affidavits
affiliate
affiliated
affiliates
affiliating
affiliation
affiliations
affinities
affinity
affirm
affirmation
affirmations
affirmative
affirmatives
affirmed
affirming
affirms
affix
affixed
affixes
affixing
afflict
afflicted
afflicting
affliction
afflictions
afflicts
affluence
affluent
afford
affordable
afforded
affording
affords
affront
affronted
affronting
affronts
afield
aflame
afloat
afoot
aforementioned
aforesaid
afraid
afresh
after
aftereffect
aftereffects
afterlife
afterlives
aftermath
aftermaths
afternoon
afternoons
afterthought
afterthoughts
afterward
afterwards
again
against
age
aged
ageing
agencies
agency
agenda
agendas
agent
agents
ages
aggravate
aggravated
aggravates
aggravating
aggravation
aggravations
aggregate
aggregated
aggregates
aggregating
aggression
aggressive
aggressively
aggressiveness
aggressor
aggressors
aghast
agile
agiler
agilest
agility
aging
agitate
agitated
agitates
agitating
agitation
agitations
agitator
agitators
aglow
agnostic
agnosticism
agnostics
ago
agonies
agonize
agonized
agonizes
agonizing
agony
agree
agreeable
agreeably
agreed
agreeing
agreement
agreements
agrees
agricultural
agriculture
aground
ah
ahead
ahoy
aid
aide
aided
aides
aiding
aids
ail
ailed
ailing
ailment
ailments
ails
aim
aimed
aiming
aimless
aimlessly
aims
air
airborne
aircraft
aired
airfield
airfields
airier
airiest
airing
airline
airliner
airliners
airlines
airmail
airmailed
airmailing
airmails
airplane
airplanes
airport
airports
airs
airstrip
airstrips
airtight
airy
aisle
aisles
ajar
akin
alarm
alarmed
alarming
alarmingly
alarmist
alarmists
alarms
alas
albeit
albino
albinos
album
albums
alcohol
alcoholic
alcoholics
alcoholism
alcohols
alcove
alcoves
ale
alert
alerted
alerting
alerts
ales
alga
algae
algebra
algebraic
algorithm
algorithms
alias
aliased
aliases
aliasing
alibi
alibied
alibiing
alibis
alien
alienate
alienated
alienates
alienating
alienation
aliened
aliening
aliens
alight
alighted
alighting
alights
align
aligned
aligning
alignment
alignments
aligns
alike
alimony
aline
alined
alinement
alinements
alines
alining
alit
alive
alkali
alkalies
alkaline
alkalis
all
allay
allayed
allaying
allays
allegation
allegations
allege
alleged
allegedly
alleges
allegiance
allegiances
alleging
allegorical
allegories
allegory
allergic
allergies
allergy
alleviate
alleviated
alleviates
alleviating
alley
alleys
alliance
alliances
allied
allies
alligator
alligators
allocate
allocated
allocates
allocating
allocation
allocations
allot
allotment
allotments
allots
allotted
allotting
allow
allowable
allowance
allowances
allowed
allowing
allows
alloy
alloyed
alloying
alloys
allude
alluded
alludes
alluding
allure
allured
allures
alluring
allusion
allusions
ally
allying
almanac
almanacs
almighty
almond
almonds
almost
alms
aloft
alone
along
alongside
aloof
aloud
alpha
alphabet
alphabetic
alphabetical
alphabetically
alphabets
alphanumeric
already
also
altar
altars
alter
alterable
alteration
alterations
altered
altering
alternate
alternated
alternately
alternates
alternating
alternation
alternative
alternatively
alternatives
alternator
alters
altho
although
altitude
altitudes
alto
altogether
altos
altruism
altruistic
aluminum
always
am
amalgamate
amalgamated
amalgamates
amalgamating
amalgamation
amalgamations
amass
amassed
amasses
amassing
amateur
amateurish
amateurs
amaze
amazed
amazement
amazes
amazing
amazingly
ambassador
ambassadors
amber
ambiance
ambiances
ambidextrous
ambience
ambiences
ambient
ambiguities
ambiguity
ambiguous
ambiguously
ambition
ambitions
ambitious
ambitiously
ambivalence
ambivalent
amble
ambled
ambles
ambling
ambulance
ambulances
ambush
ambushed
ambushes
ambushing
ameba
amebae
amebas
ameer
ameers
amen
amenable
amend
amended
amending
amendment
amendments
amends
amenities
amenity
amethyst
amethysts
amiable
amiably
amicable
amicably
amid
amidst
amir
amirs
amiss
ammonia
ammunition
amnesia
amnestied
amnesties
amnesty
amnestying
amoeba
amoebae
amoebas
amok
among
amongst
amoral
amorous
amorphous
amount
amounted
amounting
amounts
amp
ampere
amperes
ampersand
ampersands
amphetamine
amphetamines
amphibian
amphibians
amphibious
amphitheater
amphitheaters
amphitheatre
amphitheatres
ample
ampler
amplest
amplification
amplifications
amplified
amplifier
amplifiers
amplifies
amplify
amplifying
amplitude
amply
amps
amputate
amputated
amputates
amputating
amputation
amputations
amuck
amulet
amulets
amuse
amused
amusement
amusements
amuses
amusing
amusingly
an
anachronism
anachronisms
anaemia
anaemic
anaesthesia
anaesthetic
anaesthetics
anagram
anal
analgesic
analgesics
analog
analogies
analogous
analogue
analogy
analyses
analysis
analyst
analysts
analytic
analytical
analyze
analyzed
analyzer
analyzes
analyzing
anarchic
anarchism
anarchist
anarchists
anarchy
anathema
anatomical
anatomies
anatomy
ancestor
ancestors
ancestral
ancestries
ancestry
anchor
anchorage
anchorages
anchored
anchoring
anchors
anchovies
anchovy
ancient
ancienter
ancientest
ancients
and
android
androids
anecdota
anecdote
anecdotes
anemia
anemic
anesthesia
anesthetic
anesthetics
anew
angel
angelic
angels
anger
angered
angering
angers
angle
angled
angler
anglers
angles
angling
angrier
angriest
angrily
angry
angst
anguish
anguished
anguishes
anguishing
angular
ani
animal
animals
animate
animated
animates
animating
animation
animations
animosities
animosity
ankle
ankles
annals
annex
annexation
annexations
annexed
annexes
annexing
annihilate
annihilated
annihilates
annihilating
annihilation
anniversaries
anniversary
annotate
annotated
annotates
annotating
annotation
annotations
announce
announced
announcement
announcements
announcer
announcers
announces
announcing
annoy
annoyance
annoyances
annoyed
annoying
annoyingly
annoys
annual
annually
annuals
annuities
annuity
annul
annulled
annulling
annulment
annulments
annuls
anoint
anointed
anointing
anoints
anomalies
anomalous
anomaly
anon
anonymity
anonymous
anonymously
anorak
anoraks
another
answer
answerable
answered
answering
answers
ant
antagonism
antagonisms
antagonist
antagonistic
antagonists
antagonize
antagonized
antagonizes
antagonizing
anteater
anteaters
antelope
antelopes
antenna
antennae
antennas
anthem
anthems
anthill
anthills
anthologies
anthology
anthrax
anthropological
anthropologist
anthropologists
anthropology
antibiotic
antibiotics
antibodies
antibody
antic
anticipate
anticipated
anticipates
anticipating
anticipation
anticipations
anticlimax
anticlimaxes
antics
antidote
antidotes
antifreeze
antipathies
antipathy
antiquate
antiquated
antiquates
antiquating
antique
antiqued
antiques
antiquing
antiquities
antiquity
antiseptic
antiseptics
antisocial
antitheses
antithesis
antler
antlers
antonym
antonyms
ants
anus
anuses
anvil
anvils
anxieties
anxiety
anxious
anxiously
any
anybodies
anybody
anyhow
anyone
anyplace
anything
anythings
anyway
anywhere
aorta
aortae
aortas
apart
apartheid
apartment
apartments
apathetic
apathy
ape
aped
aperture
apertures
apes
apex
apexes
aphorism
aphorisms
apices
apiece
aping
aplomb
apocryphal
apologetic
apologetically
apologies
apologize
apologized
apologizes
apologizing
apology
apostle
apostles
apostrophe
apostrophes
appal
appall
appalled
appalling
appallingly
appalls
appals
apparatus
apparatuses
apparel
appareled
appareling
apparelled
apparelling
apparels
apparent
apparently
apparition
apparitions
appeal
appealed
appealing
appeals
appear
appearance
appearances
appeared
appearing
appears
appease
appeased
appeasement
appeasements
appeases
appeasing
append
appendage
appendages
appended
appendices
appendicitis
appending
appendix
appendixes
appends
appetite
appetites
appetizer
appetizers
appetizing
applaud
applauded
applauding
applauds
applause
apple
apples
appliance
appliances
applicability
applicable
applicant
applicants
application
applications
applicator
applicators
applied
applies
apply
applying
appoint
appointed
appointee
appointees
appointing
appointment
appointments
appoints
apposite
appraisal
appraisals
appraise
appraised
appraises
appraising
appreciable
appreciate
appreciated
appreciates
appreciating
appreciation
appreciations
appreciative
apprehend
apprehended
apprehending
apprehends
apprehension
apprehensions
apprehensive
apprentice
apprenticed
apprentices
apprenticeship
apprenticeships
apprenticing
approach
approachable
approached
approaches
approaching
appropriate
appropriated
appropriately
appropriates
appropriating
appropriation
appropriations
approval
approvals
approve
approved
approves
approving
approximate
approximated
approximately
approximates
approximating
approximation
approximations
apricot
apricots
apron
aprons
apt
apter
aptest
aptitude
aptitudes
aptly
aquamarine
aquamarines
aquaria
aquarium
aquariums
aquatic
aquatics
aqueduct
aqueducts
arable
arbiter
arbiters
arbitrarily
arbitrary
arbitrate
arbitrated
arbitrates
arbitrating
arbitration
arbitrator
arbitrators
arbor
arbors
arc
arcade
arcades
arcane
arced
arch
archaeological
archaeologist
archaeologists
archaeology
archaic
archbishop
archbishops
arched
archeological
archeologist
archeologists
archeology
archer
archers
archery
arches
archest
archetypal
arching
archipelago
archipelagoes
archipelagos
architect
architects
architectural
architecture
architectures
archive
archived
archives
archiving
archway
archways
arcing
arcked
arcking
arcs
ardent
ardently
ardor
ardors
arduous
arduously
are
area
areas
arena
arenas
ares
arguable
arguably
argue
argued
argues
arguing
argument
argumentative
arguments
aria
arias
arid
arise
arisen
arises
arising
aristocracies
aristocracy
aristocrat
aristocratic
aristocrats
arithmetic
ark
arks
arm
armadillo
armadillos
armament
armaments
armchair
armchairs
armed
armies
arming
armistice
armistices
armor
armored
armories
armoring
armors
armory
armpit
armpits
arms
army
aroma
aromas
aromatic
aromatics
arose
around
arouse
aroused
arouses
arousing
arraign
arraigned
arraigning
arraigns
arrange
arranged
arrangement
arrangements
arranges
arranging
array
arrayed
arraying
arrays
arrears
arrest
arrested
arresting
arrests
arrival
arrivals
arrive
arrived
arrives
arriving
arrogance
arrogant
arrogantly
arrow
arrows
arsenal
arsenals
arsenic
arson
art
artefact
artefacts
arterial
arteries
artery
artful
arthritic
arthritics
arthritis
artichoke
artichokes
article
articles
articulate
articulated
articulately
articulates
articulating
articulation
articulations
artifact
artifacts
artifice
artifices
artificial
artificially
artillery
artisan
artisans
artist
artistic
artistically
artistry
artists
arts
artwork
as
asbestos
ascend
ascended
ascending
ascends
ascension
ascensions
ascent
ascents
ascertain
ascertained
ascertaining
ascertains
ascetic
ascetics
ascribe
ascribed
ascribes
ascribing
asexual
ash
ashamed
ashcan
ashed
ashen
ashes
ashing
ashore
ashtray
ashtrays
aside
asides
ask
askance
asked
askew
asking
asks
asleep
asparagus
aspect
aspects
aspen
aspens
aspersion
aspersions
asphalt
asphalted
asphalting
asphalts
asphyxiate
asphyxiated
asphyxiates
asphyxiating
asphyxiation
asphyxiations
aspirant
aspirants
aspiration
aspirations
aspire
aspired
aspires
aspirin
aspiring
aspirins
ass
assail
assailant
assailants
assailed
assailing
assails
assassin
assassinate
assassinated
assassinates
assassinating
assassination
assassinations
assassins
assault
assaulted
assaulter
assaulting
assaults
assemble
assembled
assembler
assemblers
assembles
assemblies
assembling
assembly
assent
assented
assenting
assents
assert
asserted
asserting
assertion
assertions
assertive
asserts
asses
assess
assessed
assesses
assessing
assessment
assessments
assessor
assessors
asset
assets
assign
assigned
assigning
assignment
assignments
assigns
assimilate
assimilated
assimilates
assimilating
assimilation
assist
assistance
assistant
assistants
assisted
assisting
assists
associate
associated
associates
associating
association
associations
associative
assort
assorted
assorting
assortment
assortments
assorts
assume
assumed
assumes
assuming
assumption
assumptions
assurance
assurances
assure
assured
assureds
assures
assuring
asterisk
asterisked
asterisking
asterisks
asteroid
asteroids
asthma
astonish
astonished
astonishes
astonishing
astonishingly
astonishment
astound
astounded
astounding
astounds
astray
astride
astringent
astringents
astrological
astrology
astronaut
astronauts
astronomer
astronomers
astronomical
astronomy
astute
astutely
astuter
astutest
asylum
asylums
asymmetry
asynchronous
asynchronously
at
ate
atheism
atheist
atheistic
atheists
athlete
athletes
athletic
athletics
atlas
atlases
atmosphere
atmospheres
atmospheric
atom
atomic
atoms
atone
atoned
atonement
atones
atoning
atrocious
atrociously
atrocities
atrocity
attach
attached
attaching
attachment
attachments
attack
attacked
attacker
attacking
attacks
attain
attained
attaining
attainment
attainments
attains
attempt
attempted
attempting
attempts
attend
attendance
attendances
attendant
attendants
attended
attending
attends
attention
attentions
attentive
attentively
attest
attested
attesting
attests
attic
attics
attire
attired
attires
attiring
attitude
attitudes
attorney
attorneys
attract
attracted
attracting
attraction
attractions
attractive
attractiveness
attracts
attributable
attribute
attributed
attributes
attributing
attribution
attune
attuned
attunes
attuning
auburn
auction
auctioned
auctioneer
auctioneers
auctioning
auctions
audacious
audacity
audible
audibles
audibly
audience
audiences
audio
audios
audit
audited
auditing
audition
auditioned
auditioning
auditions
auditor
auditoria
auditorium
auditoriums
auditors
auditory
audits
augment
augmented
augmenting
augments
august
auguster
augustest
aunt
aunts
aura
aurae
aural
auras
auspicious
austere
austerer
austerest
austerities
austerity
authentic
authentically
authenticate
authenticated
authenticates
authenticating
authenticity
author
authored
authoring
authoritarian
authoritative
authoritatively
authorities
authority
authorization
authorizations
authorize
authorized
authorizes
authorizing
authors
authorship
auto
autobiographical
autobiographies
autobiography
autocracies
autocracy
autocrat
autocratic
autocrats
autograph
autographed
autographing
autographs
automate
automated
automates
automatic
automatically
automatics
automating
automation
automobile
automobiled
automobiles
automobiling
automotive
autonomous
autonomy
autopsied
autopsies
autopsy
autopsying
autos
autumn
autumnal
autumns
auxiliaries
auxiliary
avail
availability
available
availed
availing
avails
avalanche
avalanches
avarice
avaricious
avenge
avenged
avenges
avenging
avenue
avenues
average
averaged
averages
averaging
averse
aversion
aversions
avert
averted
averting
averts
aviation
aviator
aviators
avid
avocado
avocadoes
avocados
avoid
avoidable
avoidance
avoided
avoiding
avoids
avow
avowal
avowals
avowed
avowing
avows
await
awaited
awaiting
awaits
awake
awaked
awaken
awakened
awakening
awakens
awakes
awaking
award
awarded
awarding
awards
aware
awareness
away
awe
awed
awes
awesome
awful
awfuller
awfullest
awfully
awhile
awing
awkward
awkwarder
awkwardest
awkwardly
awkwardness
awning
awnings
awoke
awoken
awry
ax
axe
axed
axes
axing
axiom
axiomatic
axioms
axis
axle
axles
ay
aye
ayes
azalea
azaleas
azure
azures
babble
babbled
babbles
babbling
babe
babes
babied
babier
babies
babiest
baboon
baboons
baby
babying
babyish
bachelor
bachelors
back
backbone
backbones
backed
backer
backers
backfire
backfired
backfires
backfiring
backgammon
background
backgrounds
backhand
backhanded
backhanding
backhands
backing
backings
backlash
backlashes
backlog
backlogged
backlogging
backlogs
backpack
backpacked
backpacking
backpacks
backs
backside
backslash
backspace
backstage
backtrack
backtracked
backtracking
backtracks
backward
backwards
backwoods
bacon
bacteria
bacterial
bacterias
bacterium
bad
badder
baddest
bade
badge
badger
badgered
badgering
badgers
badges
badly
badminton
badness
baffle
baffled
baffles
baffling
bag
bagel
bagels
baggage
bagged
baggier
baggiest
bagging
baggy
bags
bail
bailed
bailing
bails
bait
baited
baiting
baits
bake
baked
baker
bakeries
bakers
bakery
bakes
baking
balance
balanced
balances
balancing
balconies
balcony
bald
balded
balder
baldest
balding
baldness
balds
bale
baled
bales
baling
balk
balked
balking
balks
ball
ballad
ballads
ballast
ballasted
ballasting
ballasts
balled
ballerina
ballerinas
ballet
ballets
balling
ballistics
balloon
ballooned
ballooning
balloons
ballot
balloted
balloting
ballots
ballroom
ballrooms
balls
balm
balmier
balmiest
balms
balmy
baloney
bamboo
bamboos
bamboozle
bamboozled
bamboozles
bamboozling
ban
banal
banana
bananas
band
bandage
bandaged
bandages
bandaging
bandana
bandanas
bandanna
bandannas
banded
bandied
bandier
bandies
bandiest
banding
bandit
bandits
banditti
bands
bandstand
bandstands
bandwagon
bandwagons
bandwidth
bandy
bandying
bang
banged
banging
bangs
bani
banish
banished
banishes
banishing
banister
banisters
banjo
banjoes
banjos
bank
banked
banker
bankers
banking
banknote
banknotes
bankrupt
bankruptcies
bankruptcy
bankrupted
bankrupting
bankrupts
banks
banned
banner
banners
banning
bannister
bannisters
banquet
banqueted
banqueting
banquets
bans
banter
bantered
bantering
banters
baptism
baptisms
baptize
baptized
baptizes
baptizing
bar
barb
barbarian
barbarians
barbaric
barbarous
barbecue
barbecued
barbecues
barbecuing
barbed
barbeque
barbequed
barbeques
barbequing
barber
barbered
barbering
barbers
barbing
barbiturate
barbiturates
barbs
bard
bards
bare
bareback
bared
barefoot
barely
barer
bares
barest
bargain
bargained
bargainer
bargaining
bargains
barge
barged
barges
barging
baring
baritone
baritones
bark
barked
barking
barks
barley
barman
barn
barnacle
barnacles
barns
barnyard
barnyards
barometer
barometers
baron
barons
baroque
barrage
barraged
barrages
barraging
barred
barrel
barreled
barreling
barrelled
barrelling
barrels
barren
barrener
barrenest
barrens
barrette
barrettes
barricade
barricaded
barricades
barricading
barrier
barriers
barring
barrings
barrister
barristers
bars
bartender
bartenders
barter
bartered
bartering
barters
base
baseball
baseballs
based
baseline
basement
basements
baser
bases
basest
bash
bashed
bashes
bashful
bashing
basic
basically
basics
basil
basin
basing
basins
basis
bask
basked
basket
basketball
basketballs
baskets
basking
basks
bass
basses
bassoon
bassoons
bastard
bastards
baste
basted
bastes
basting
bat
batch
batched
batches
batching
bath
bathe
bathed
bathes
bathing
bathroom
bathrooms
baths
bathtub
bathtubs
baton
batons
bats
batsman
battalion
battalions
batted
batter
battered
batteries
battering
batters
battery
batting
battle
battled
battlefield
battlefields
battles
battleship
battleships
battling
baud
bauds
bawdier
bawdiest
bawdy
bawl
bawled
bawling
bawls
bay
bayed
baying
bayonet
bayoneted
bayoneting
bayonets
bayonetted
bayonetting
bayou
bayous
bays
bazaar
bazaars
be
beach
beached
beaches
beaching
beacon
beacons
bead
beaded
beadier
beadiest
beading
beads
beady
beagle
beagles
beak
beaked
beaker
beakers
beaks
beam
beamed
beaming
beams
bean
beaned
beaning
beans
bear
bearable
beard
bearded
bearding
beards
bearer
bearers
bearing
bearings
bears
beast
beasts
beat
beaten
beater
beaters
beating
beats
beautician
beauticians
beauties
beautified
beautifies
beautiful
beautifully
beautify
beautifying
beauty
beaver
beavered
beavering
beavers
became
because
beckon
beckoned
beckoning
beckons
become
becomes
becoming
bed
bedbug
bedbugs
bedclothes
bedded
bedder
bedding
bedlam
bedlams
bedridden
bedrock
bedrocks
bedroom
bedrooms
beds
bedside
bedsides
bedspread
bedspreads
bedtime
bedtimes
bee
beech
beeches
beef
beefed
beefier
beefiest
beefing
beefs
beefy
beehive
beehives
been
beeper
beer
beers
bees
beeswax
beet
beetle
beetled
beetles
beetling
beets
beeves
befall
befallen
befalling
befalls
befell
befit
befits
befitted
befitting
before
beforehand
befriend
befriended
befriending
befriends
beg
began
beggar
beggared
beggaring
beggars
begged
begging
begin
beginner
beginners
beginning
beginnings
begins
begrudge
begrudged
begrudges
begrudging
begs
beguile
beguiled
beguiles
beguiling
begun
behalf
behalves
behave
behaved
behaves
behaving
behavior
behavioral
behead
beheaded
beheading
beheads
beheld
behind
behinds
behold
beholder
beholding
beholds
beige
being
beings
belabor
belabored
belaboring
belabors
belated
belatedly
belch
belched
belches
belching
belfries
belfry
belie
belied
belief
beliefs
belies
believable
believe
believed
believer
believers
believes
believing
belittle
belittled
belittles
belittling
bell
bellboy
bellboys
belled
bellhop
bellhops
bellied
bellies
belligerent
belligerents
belling
bellow
bellowed
bellowing
bellows
bells
belly
bellying
belong
belonged
belonging
belongings
belongs
beloved
beloveds
below
belt
belted
belting
belts
belying
bemoan
bemoaned
bemoaning
bemoans
bemuse
bemused
bemuses
bemusing
bench
benched
benches
benching
bend
bender
bending
bends
beneath
benediction
benedictions
benefactor
benefactors
beneficial
beneficiaries
beneficiary
benefit
benefited
benefiting
benefits
benefitted
benefitting
benevolence
benevolences
benevolent
benighted
benign
bent
bents
bequeath
bequeathed
bequeathing
bequeaths
bequest
bequests
bereave
bereaved
bereavement
bereavements
bereaves
bereaving
bereft
beret
berets
berried
berries
berry
berrying
berserk
berth
berthed
berthing
berths
beseech
beseeched
beseeches
beseeching
beset
besets
besetting
beside
besides
besiege
besieged
besieges
besieging
besought
best
bested
bestial
bestiality
besting
bestow
bestowed
bestowing
bestows
bests
bet
beta
betcha
betray
betrayal
betrayals
betrayed
betraying
betrays
betrothal
betrothals
bets
betted
better
bettered
bettering
betterment
betters
betting
bettor
bettors
between
beverage
beverages
beware
bewared
bewares
bewaring
bewilder
bewildered
bewildering
bewilderment
bewilders
bewitch
bewitched
bewitches
bewitching
beyond
bias
biased
biases
biasing
biassed
biassing
bib
bible
biblical
bibliographic
bibliographies
bibliography
bibs
bicentennial
bicentennials
bicker
bickered
bickering
bickers
bicycle
bicycled
bicycles
bicycling
bid
bidden
bidding
bide
bided
bides
biding
bids
biennial
biennials
bifocals
big
bigamist
bigamists
bigamous
bigamy
bigger
biggest
bigot
bigoted
bigotry
bigots
bike
biked
bikes
biking
bikini
bikinis
bilateral
bile
bilingual
bilinguals
bill
billboard
billboards
billed
billfold
billfolds
billiards
billing
billion
billions
billow
billowed
billowing
billows
bills
bin
binaries
binary
bind
binder
binders
binding
bindings
binds
bingo
binned
binning
binomial
bins
biochemical
biochemistry
biodegradable
biographer
biographers
biographical
biographies
biography
biological
biologically
biologist
biologists
biology
bipartisan
biped
bipeds
biplane
biplanes
birch
birched
birches
birching
bird
birdcage
birdcages
birded
birding
birds
birth
birthday
birthdays
birthed
birthing
birthmark
birthmarks
birthplace
birthplaces
births
biscuit
biscuits
bisect
bisected
bisecting
bisects
bisexual
bisexuals
bishop
bishops
bison
bisons
bit
bitch
bitched
bitches
bitching
bite
bites
biting
bitmap
bits
bitten
bitter
bitterer
bitterest
bitterly
bitterness
bittersweet
bittersweets
bizarre
blab
blabbed
blabbing
blabs
black
blackberries
blackberry
blackberrying
blackbird
blackbirds
blackboard
blackboards
blacked
blacken
blackened
blackening
blackens
blacker
blackest
blackhead
blackheads
blacking
blackjack
blackjacked
blackjacking
blackjacks
blacklist
blacklisted
blacklisting
blacklists
blackmail
blackmailed
blackmailer
blackmailers
blackmailing
blackmails
blackout
blackouts
blacks
blacksmith
blacksmiths
blacktop
blacktopped
blacktopping
blacktops
bladder
bladders
blade
blades
blame
blamed
blameless
blamer
blames
blaming
blanch
blanched
blanches
blanching
blancmange
bland
blander
blandest
blank
blanked
blanker
blankest
blanket
blanketed
blanketing
blankets
blanking
blankly
blanks
blare
blared
blares
blaring
blaspheme
blasphemed
blasphemes
blasphemies
blaspheming
blasphemous
blasphemy
blast
blasted
blaster
blasting
blasts
blatant
blatantly
blaze
blazed
blazer
blazers
blazes
blazing
bleach
bleached
bleaches
bleaching
bleak
bleaker
bleakest
blearier
bleariest
bleary
bleat
bleated
bleating
bleats
bled
bleed
bleeding
bleeds
blemish
blemished
blemishes
blemishing
blend
blended
blending
blends
blent
bless
blessed
blesses
blessing
blessings
blest
blew
blight
blighted
blighting
blights
blimp
blimps
blind
blinded
blinder
blindest
blindfold
blindfolded
blindfolding
blindfolds
blinding
blindingly
blindly
blindness
blinds
blink
blinked
blinker
blinkered
blinkering
blinkers
blinking
blinks
blip
blips
bliss
blissful
blissfully
blister
blistered
blistering
blisters
blithe
blithely
blither
blithest
blitz
blitzed
blitzes
blitzing
blizzard
blizzards
blob
blobbed
blobbing
blobs
bloc
block
blockade
blockaded
blockades
blockading
blockage
blockbuster
blockbusters
blocked
blockhead
blockheads
blocking
blocks
blocs
blog
blogged
blogger
bloggers
blogging
blogs
blond
blonde
blonder
blondes
blondest
blonds
blood
blooded
bloodhound
bloodhounds
bloodied
bloodier
bloodies
bloodiest
blooding
bloods
bloodshed
bloodshot
bloodstream
bloodthirstier
bloodthirstiest
bloodthirsty
bloody
bloodying
bloom
bloomed
blooming
blooms
blossom
blossomed
blossoming
blossoms
blot
blotch
blotched
blotches
blotching
blots
blotted
blotter
blotters
blotting
blouse
bloused
blouses
blousing
blow
blowing
blown
blowout
blowouts
blows
blowtorch
blowtorches
blubber
blubbered
blubbering
blubbers
bludgeon
bludgeoned
bludgeoning
bludgeons
blue
bluebell
bluebells
blueberries
blueberry
bluebird
bluebirds
blued
bluegrass
blueing
blueprint
blueprinted
blueprinting
blueprints
bluer
blues
bluest
bluff
bluffed
bluffer
bluffest
bluffing
bluffs
bluing
blunder
blundered
blundering
blunders
blunt
blunted
blunter
bluntest
blunting
bluntly
bluntness
blunts
blur
blurb
blurred
blurring
blurs
blurt
blurted
blurting
blurts
blush
blushed
blushes
blushing
bluster
blustered
blustering
blusters
boa
boar
board
boarded
boarder
boarders
boarding
boards
boardwalk
boardwalks
boars
boas
boast
boasted
boastful
boastfully
boasting
boasts
boat
boated
boating
boats
bob
bobbed
bobbin
bobbing
bobbins
bobcat
bobcats
bobs
bobsled
bobsledded
bobsledding
bobsleds
bode
boded
bodes
bodice
bodices
bodies
bodily
boding
body
bodyguard
bodyguards
bodywork
bog
bogged
bogging
boggle
boggled
boggles
boggling
bogs
bogus
boil
boiled
boiler
boilers
boiling
boils
boisterous
bold
bolder
boldest
boldly
boldness
bologna
boloney
bolster
bolstered
bolstering
bolsters
bolt
bolted
bolting
bolts
bomb
bombard
bombarded
bombarding
bombardment
bombardments
bombards
bombed
bomber
bombers
bombing
bombings
bombs
bond
bondage
bonded
bonding
bonds
bone
boned
bones
boney
boneyer
boneyest
bonfire
bonfires
bonier
boniest
boning
bonnet
bonnets
bonus
bonuses
bony
boo
booby
booed
booing
book
bookcase
bookcases
booked
bookend
bookends
booking
bookings
bookkeeper
bookkeepers
bookkeeping
booklet
booklets
bookmark
bookmarked
bookmarking
bookmarks
books
bookshelf
bookshop
bookshops
bookstore
bookworm
bookworms
boom
boomed
boomerang
boomeranged
boomeranging
boomerangs
booming
booms
boon
boons
boor
boorish
boors
boos
boost
boosted
booster
boosters
boosting
boosts
boot
booted
bootee
bootees
booth
booths
bootie
booties
booting
bootleg
bootlegged
bootlegging
bootlegs
boots
bootstrap
booty
booze
bop
border
bordered
bordering
borderline
borderlines
borders
bore
bored
boredom
bores
boring
boringly
born
borne
borough
boroughs
borrow
borrowed
borrowing
borrows
bosom
bosoms
boss
bossed
bosses
bossier
bossiest
bossing
bossy
botanical
botanist
botanists
botany
botch
botched
botches
botching
both
bother
bothered
bothering
bothers
bothersome
bottle
bottled
bottleneck
bottlenecks
bottles
bottling
bottom
bottomed
bottoming
bottomless
bottoms
bough
boughs
bought
boulder
boulders
boulevard
boulevards
bounce
bounced
bounces
bouncing
bound
boundaries
boundary
bounded
bounding
boundless
bounds
bounties
bountiful
bounty
bouquet
bouquets
bourbon
bourgeois
bourgeoisie
bout
boutique
boutiques
bouts
bovine
bovines
bow
bowed
bowel
bowels
bowing
bowl
bowlder
bowlders
bowled
bowlegged
bowler
bowling
bowls
bows
box
boxcar
boxcars
boxed
boxer
boxers
boxes
boxing
boy
boycott
boycotted
boycotting
boycotts
boyfriend
boyfriends
boyhood
boyhoods
boyish
boys
bra
brace
braced
bracelet
bracelets
braces
bracing
bracket
bracketed
bracketing
brackets
brackish
brag
braggart
braggarts
bragged
bragging
brags
braid
braided
braiding
braids
brain
brained
brainier
brainiest
braining
brainless
brains
brainstorm
brainstormed
brainstorming
brainstorms
brainwash
brainwashed
brainwashes
brainwashing
brainy
braise
braised
braises
braising
brake
braked
brakes
braking
bran
branch
branched
branches
branching
brand
branded
brandied
brandies
branding
brandish
brandished
brandishes
brandishing
brands
brandy
brandying
bras
brash
brasher
brashest
brass
brasses
brassier
brassiere
brassieres
brassiest
brassy
brat
brats
bravado
brave
braved
bravely
braver
bravery
braves
bravest
braving
bravo
bravos
brawl
brawled
brawling
brawls
brawn
brawnier
brawniest
brawny
bray
brayed
braying
brays
brazen
brazened
brazening
brazens
brazier
braziers
breach
breached
breaches
breaching
bread
breaded
breading
breads
breadth
breadths
breadwinner
breadwinners
break
breakable
breakables
breakdown
breakdowns
breakfast
breakfasted
breakfasting
breakfasts
breaking
breakneck
breakpoints
breaks
breakthrough
breakthroughs
breakwater
breakwaters
breast
breasted
breasting
breasts
breath
breathe
breathed
breather
breathers
breathes
breathing
breathless
breaths
breathtaking
bred
breed
breeder
breeders
breeding
breeds
breeze
breezed
breezes
breezier
breeziest
breezing
breezy
brethren
brevity
brew
brewed
breweries
brewery
brewing
brews
bribe
bribed
bribery
bribes
bribing
brick
bricked
bricking
bricklayer
bricklayers
bricks
bridal
bridals
bride
bridegroom
bridegrooms
brides
bridesmaid
bridesmaids
bridge
bridged
bridges
bridging
bridle
bridled
bridles
bridling
brief
briefcase
briefcases
briefed
briefer
briefest
briefing
briefly
briefs
brigade
brigades
bright
brighten
brightened
brightening
brightens
brighter
brightest
brightly
brightness
brilliance
brilliant
brilliantly
brilliants
brim
brimmed
brimming
brims
brimstone
brine
bring
bringing
brings
brinier
briniest
brink
brinks
briny
brisk
brisked
brisker
briskest
brisking
briskly
brisks
bristle
bristled
bristles
bristling
britches
brittle
brittler
brittlest
broach
broached
broaches
broaching
broad
broadcast
broadcasted
broadcasting
broadcasts
broaden
broadened
broadening
broadens
broader
broadest
broadly
broads
broadside
broadsided
broadsides
broadsiding
brocade
brocaded
brocades
brocading
broccoli
brochure
brochures
broil
broiled
broiler
broilers
broiling
broils
broke
broken
broker
brokered
brokering
brokers
bronchitis
broncho
bronchos
bronco
broncos
bronze
bronzed
bronzes
bronzing
brooch
brooches
brood
brooded
brooding
broods
brook
brooked
brooking
brooks
broom
brooms
broth
brother
brotherhood
brotherhoods
brotherly
brothers
broths
brought
brow
browbeat
browbeaten
browbeating
browbeats
brown
browned
browner
brownest
brownie
brownies
browning
browns
brows
browse
browsed
browses
browsing
bruise
bruised
bruises
bruising
brunch
brunched
brunches
brunching
brunette
brunettes
brunt
brush
brushed
brushes
brushing
brusk
brusker
bruskest
brusque
brusquer
brusquest
brutal
brutalities
brutality
brutally
brute
brutes
brutish
bubble
bubbled
bubbles
bubblier
bubbliest
bubbling
bubbly
buck
bucked
bucket
bucketed
bucketing
buckets
bucking
buckle
buckled
buckles
buckling
bucks
bud
budded
buddies
budding
buddy
budge
budged
budges
budget
budgeted
budgeting
budgets
budging
buds
buff
buffalo
buffaloed
buffaloes
buffaloing
buffalos
buffed
buffer
buffered
buffering
buffers
buffet
buffeted
buffeting
buffets
buffing
buffoon
buffoons
buffs
bug
bugged
bugger
buggers
buggier
buggies
buggiest
bugging
buggy
bugle
bugled
bugler
buglers
bugles
bugling
bugs
build
builder
builders
building
buildings
builds
built
bulb
bulbous
bulbs
bulge
bulged
bulges
bulging
bulk
bulked
bulkier
bulkiest
bulking
bulks
bulky
bull
bulldog
bulldogged
bulldogging
bulldogs
bulldoze
bulldozed
bulldozer
bulldozers
bulldozes
bulldozing
bulled
bullet
bulletin
bulletined
bulletining
bulletins
bullets
bullfight
bullfighter
bullfighters
bullfights
bullfrog
bullfrogs
bullied
bullies
bulling
bullion
bulls
bully
bullying
bum
bumblebee
bumblebees
bummed
bummer
bummest
bumming
bump
bumped
bumper
bumpers
bumpier
bumpiest
bumping
bumps
bumpy
bums
bun
bunch
bunched
bunches
bunching
bundle
bundled
bundles
bundling
bung
bungalow
bungalows
bungle
bungled
bungler
bunglers
bungles
bungling
bunion
bunions
bunk
bunked
bunker
bunkers
bunking
bunks
bunnies
bunny
buns
buoy
buoyancy
buoyant
buoyed
buoying
buoys
burble
burbled
burbles
burbling
burden
burdened
burdening
burdens
burdensome
bureau
bureaucracies
bureaucracy
bureaucrat
bureaucratic
bureaucrats
bureaus
bureaux
burger
burgers
burglar
burglaries
burglars
burglary
burgle
burial
burials
buried
buries
burlap
burlier
burliest
burly
burn
burned
burner
burners
burning
burnish
burnished
burnishes
burnishing
burns
burnt
burp
burped
burping
burps
burr
burred
burring
burro
burros
burrow
burrowed
burrowing
burrows
burrs
bursar
burst
bursted
bursting
bursts
bury
burying
bus
bused
buses
bush
bushed
bushel
busheled
busheling
bushelled
bushelling
bushels
bushes
bushier
bushiest
bushing
bushy
busied
busier
busies
busiest
busily
business
businesses
businessman
businessmen
businesswoman
businesswomen
busing
buss
bussed
busses
bussing
bust
busted
busting
bustle
bustled
bustles
bustling
busts
busy
busybodies
busybody
busying
but
butcher
butchered
butcheries
butchering
butchers
butchery
butler
butlers
buts
butt
butte
butted
butter
buttercup
buttercups
buttered
butterflied
butterflies
butterfly
butterflying
buttering
buttermilk
butters
butterscotch
buttery
buttes
butting
buttock
buttocks
button
buttoned
buttonhole
buttonholed
buttonholes
buttonholing
buttoning
buttons
buttress
buttressed
buttresses
buttressing
butts
buxom
buy
buyer
buyers
buying
buys
buzz
buzzard
buzzards
buzzed
buzzer
buzzers
buzzes
buzzing
by
bye
byes
bygone
bygones
bypass
bypassed
bypasses
bypassing
bypast
bystander
bystanders
byte
bytes
byway
byways
cab
cabaret
cabarets
cabbage
cabbages
cabbed
cabbing
cabin
cabinet
cabinets
cabins
cable
cabled
cables
cabling
caboose
cabooses
cabs
cacao
cacaos
cache
cached
caches
caching
cackle
cackled
cackles
cackling
cacti
cactus
cactuses
cad
caddie
caddied
caddies
caddy
caddying
cadence
cadences
cadet
cadets
cafeteria
cafeterias
caffeine
cage
caged
cages
cagey
cagier
cagiest
caging
cagy
cajole
cajoled
cajoles
cajoling
cake
caked
cakes
caking
calamities
calamity
calcium
calculate
calculated
calculates
calculating
calculation
calculations
calculator
calculators
calculi
calculus
calculuses
calendar
calendared
calendaring
calendars
calf
calfs
caliber
calibers
calibrate
calibrated
calibrates
calibrating
calibration
calibrations
calico
calicoes
calicos
calk
calked
calking
calkings
calks
call
callable
called
caller
callers
calligraphy
calling
callings
callous
calloused
callouses
callousing
callow
calls
callus
callused
calluses
callusing
calm
calmed
calmer
calmest
calming
calmly
calmness
calms
calorie
calories
calve
calves
cam
camaraderie
came
camel
camels
cameo
cameos
camera
cameras
camouflage
camouflaged
camouflages
camouflaging
camp
campaign
campaigned
campaigner
campaigners
campaigning
campaigns
camped
camper
campers
camping
camps
campus
campuses
can
canal
canals
canaries
canary
cancel
cancelation
canceled
canceling
cancellation
cancellations
cancelled
cancelling
cancels
cancer
cancers
candid
candidacies
candidacy
candidate
candidates
candidly
candied
candies
candle
candled
candles
candlestick
candlesticks
candling
candor
candy
candying
cane
caned
canes
canine
canines
caning
canister
canisters
canker
cankered
cankering
cankers
canned
canneries
cannery
cannibal
cannibalism
cannibals
cannier
canniest
canning
cannon
cannoned
cannoning
cannons
cannot
canny
canoe
canoed
canoeing
canoes
canon
canonical
canons
canopied
canopies
canopy
canopying
cans
cant
cantaloup
cantaloupe
cantaloupes
cantaloups
cantankerous
canteen
canteens
canter
cantered
cantering
canters
canvas
canvased
canvases
canvasing
canvass
canvassed
canvasser
canvassers
canvasses
canvassing
canyon
canyons
cap
capabilities
capability
capable
capably
capacitance
capacities
capacitor
capacitors
capacity
cape
caped
caper
capered
capering
capers
capes
capillaries
capillary
capital
capitalism
capitalist
capitalists
capitalization
capitalize
capitalized
capitalizes
capitalizing
capitals
capitulate
capitulated
capitulates
capitulating
capped
capping
caprice
caprices
capricious
capriciously
caps
capsize
capsized
capsizes
capsizing
capsule
capsuled
capsules
capsuling
captain
captained
captaining
captains
caption
captioned
captioning
captions
captivate
captivated
captivates
captivating
captive
captives
captivities
captivity
captor
captors
capture
captured
captures
capturing
car
caramel
caramels
carat
carats
caravan
caravans
carbohydrate
carbohydrates
carbon
carbons
carburetor
carburetors
carcass
carcasses
carcinogenic
card
cardboard
carded
cardiac
cardigan
cardigans
cardinal
cardinals
carding
cards
care
cared
career
careered
careering
careers
carefree
careful
carefuller
carefullest
carefully
carefulness
careless
carelessly
carelessness
cares
caress
caressed
caresses
caressing
caretaker
caretakers
cargo
cargoes
cargos
caribou
caribous
caricature
caricatured
caricatures
caricaturing
caring
carnage
carnal
carnation
carnations
carnival
carnivals
carnivore
carnivores
carnivorous
carol
caroled
caroling
carolled
carolling
carols
carouse
caroused
carouses
carousing
carp
carped
carpenter
carpentered
carpentering
carpenters
carpentry
carpet
carpeted
carpeting
carpets
carping
carps
carriage
carriages
carriageway
carried
carrier
carriers
carries
carrion
carrot
carrots
carry
carrying
cars
cart
carted
cartel
cartels
cartilage
cartilages
carting
cartographer
cartographers
cartography
carton
cartons
cartoon
cartooned
cartooning
cartoonist
cartoonists
cartoons
cartridge
cartridges
carts
cartwheel
cartwheeled
cartwheeling
cartwheels
carve
carved
carves
carving
cascade
cascaded
cascades
cascading
case
cased
cases
cash
cashed
cashes
cashew
cashews
cashier
cashiered
cashiering
cashiers
cashing
cashmere
casing
casings
casino
casinos
cask
casket
caskets
casks
casserole
casseroled
casseroles
casseroling
cassette
cassettes
cassino
cassinos
cast
castaway
castaways
caste
caster
casters
castes
castigate
castigated
castigates
castigating
casting
castings
castle
castled
castles
castling
castoff
castoffs
castrate
castrated
castrates
castrating
casts
casual
casually
casuals
casualties
casualty
cat
cataclysm
cataclysmic
cataclysms
catalog
cataloged
cataloging
catalogs
catalogue
catalogued
catalogues
cataloguing
catapult
catapulted
catapulting
catapults
cataract
cataracts
catastrophe
catastrophes
catastrophic
catcall
catcalled
catcalling
catcalls
catch
catches
catchier
catchiest
catching
catchings
catchment
catchup
catchy
catechism
catechisms
categorical
categorically
categories
categorize
categorized
categorizes
categorizing
category
cater
catered
caterer
caterers
catering
caterpillar
caterpillars
caters
catfish
catfishes
cathedral
cathedrals
catholic
catnap
catnapped
catnapping
catnaps
catnip
cats
catsup
cattle
catwalk
catwalks
caucus
caucused
caucuses
caucusing
caucussed
caucussing
caught
cauliflower
cauliflowers
caulk
caulked
caulking
caulkings
caulks
causal
causality
cause
caused
causes
causeway
causeways
causing
caustic
caustics
caution
cautioned
cautioning
cautions
cautious
cautiously
cavalier
cavaliers
cavalries
cavalry
cave
caveat
caveats
caved
cavern
caverns
caves
caviar
caviare
caving
cavities
cavity
cavort
cavorted
cavorting
cavorts
caw
cawed
cawing
caws
cease
ceased
ceasefire
ceaseless
ceaselessly
ceases
ceasing
cedar
cedars
cede
ceded
cedes
ceding
ceiling
ceilings
celebrate
celebrated
celebrates
celebrating
celebration
celebrations
celebrities
celebrity
celery
celestial
celibacy
celibate
celibates
cell
cellar
cellars
celli
cellist
cellists
cello
cellophane
cellos
cells
cellular
cellulars
cellulose
cement
cemented
cementing
cements
cemeteries
cemetery
censor
censored
censoring
censors
censorship
censure
censured
censures
censuring
census
censused
censuses
censusing
cent
centennial
centennials
center
centered
centering
centerpiece
centerpieces
centers
centimeter
centimeters
centipede
centipedes
central
centralize
centralized
centralizes
centralizing
centrally
centrals
centrifuge
cents
centuries
century
ceramic
cereal
cereals
cerebral
ceremonial
ceremonials
ceremonies
ceremonious
ceremony
certain
certainly
certainties
certainty
certificate
certificated
certificates
certificating
certified
certifies
certify
certifying
cervical
cessation
cessations
chafe
chafed
chafes
chaff
chaffed
chaffing
chaffs
chafing
chagrin
chagrined
chagrining
chagrinned
chagrinning
chagrins
chain
chained
chaining
chains
chainsaw
chair
chaired
chairing
chairman
chairmen
chairperson
chairpersons
chairs
chalet
chalets
chalice
chalices
chalk
chalked
chalkier
chalkiest
chalking
chalks
chalky
challenge
challenged
challenger
challengers
challenges
challenging
chamber
chambers
chameleon
chameleons
champ
champagne
champagnes
champed
champing
champion
championed
championing
champions
championship
championships
champs
chance
chanced
chancellor
chancellors
chances
chancing
chandelier
chandeliers
change
changeable
changed
changeover
changes
changing
channel
channeled
channeling
channelled
channelling
channels
chant
chanted
chanting
chants
chaos
chaotic
chap
chapel
chapels
chaperon
chaperone
chaperoned
chaperones
chaperoning
chaperons
chaplain
chaplains
chapped
chapping
chaps
chapt
chapter
chapters
char
character
characteristic
characteristically
characteristics
characterization
characterize
characterized
characterizes
characterizing
characters
charcoal
charcoals
charge
chargeable
charged
charger
charges
charging
chariot
chariots
charisma
charismatic
charismatics
charitable
charitably
charities
charity
charlatan
charlatans
charm
charmed
charming
charms
charred
charring
chars
chart
charted
charter
chartered
chartering
charters
charting
charts
chase
chased
chases
chasing
chasm
chasms
chassis
chaste
chasten
chastened
chastening
chastens
chaster
chastest
chastise
chastised
chastisement
chastisements
chastises
chastising
chastity
chat
chats
chatted
chatter
chatterbox
chatterboxes
chattered
chattering
chatters
chattier
chattiest
chatting
chatty
chauffeur
chauffeured
chauffeuring
chauffeurs
chauvinist
chauvinists
cheap
cheapen
cheapened
cheapening
cheapens
cheaper
cheapest
cheaply
cheapness
cheat
cheated
cheating
cheats
check
checked
checker
checkers
checking
checkout
checkpoint
checks
checkup
checkups
cheek
cheeked
cheeking
cheeks
cheep
cheeped
cheeping
cheeps
cheer
cheered
cheerful
cheerfuller
cheerfullest
cheerfully
cheerfulness
cheerier
cheeriest
cheering
cheers
cheery
cheese
cheesecloth
cheesed
cheeses
cheesing
cheetah
cheetahs
chef
chefs
chemical
chemically
chemicals
chemist
chemistry
chemists
cherish
cherished
cherishes
cherishing
cherries
cherry
cherub
cherubim
cherubims
cherubs
chess
chest
chestnut
chestnuts
chests
chew
chewed
chewier
chewiest
chewing
chews
chewy
chi
chic
chicer
chicest
chick
chicken
chickened
chickening
chickens
chicks
chid
chidden
chide
chided
chides
chiding
chief
chiefer
chiefest
chiefly
chiefs
chieftain
chieftains
child
childbirth
childbirths
childhood
childhoods
childish
childlike
children
chile
chiles
chili
chilies
chilis
chill
chilled
chiller
chillest
chilli
chillier
chillies
chilliest
chilling
chills
chilly
chime
chimed
chimes
chiming
chimney
chimneys
chimp
chimpanzee
chimpanzees
chimps
chin
china
chink
chinked
chinking
chinks
chinned
chinning
chins
chintz
chip
chipmunk
chipmunks
chipped
chipper
chippers
chipping
chips
chiropractor
chiropractors
chirp
chirped
chirping
chirps
chisel
chiseled
chiseling
chiselled
chiselling
chisels
chivalrous
chivalry
chlorine
chloroform
chloroformed
chloroforming
chloroforms
chlorophyll
chocolate
chocolates
choice
choicer
choices
choicest
choir
choirs
choke
choked
chokes
choking
cholera
cholesterol
choose
chooses
choosey
choosier
choosiest
choosing
choosy
chop
chopped
chopper
choppered
choppering
choppers
choppier
choppiest
chopping
choppy
chops
choral
chorals
chord
chords
chore
choreographer
choreographers
choreography
chores
chortle
chortled
chortles
chortling
chorus
chorused
choruses
chorusing
chorussed
chorussing
chose
chosen
chow
chowder
chowders
chowed
chowing
chows
christen
christened
christening
christenings
christens
chrome
chromed
chromes
chroming
chromium
chromosome
chromosomes
chronic
chronically
chronicle
chronicled
chronicles
chronicling
chronological
chronologically
chronologies
chronology
chrysanthemum
chrysanthemums
chubbier
chubbiest
chubby
chuck
chucked
chucking
chuckle
chuckled
chuckles
chuckling
chucks
chug
chugged
chugging
chugs
chum
chummed
chummier
chummiest
chumming
chummy
chums
chunk
chunkier
chunkiest
chunks
chunky
church
churches
churn
churned
churning
churns
chute
chutes
cider
ciders
cigar
cigaret
cigarets
cigarette
cigarettes
cigars
cinch
cinched
cinches
cinching
cinder
cindered
cindering
cinders
cinema
cinemas
cinnamon
cipher
ciphered
ciphering
ciphers
circa
circle
circled
circles
circling
circuit
circuited
circuiting
circuitous
circuitry
circuits
circular
circulars
circulate
circulated
circulates
circulating
circulation
circulations
circulatory
circumcise
circumcised
circumcises
circumcising
circumcision
circumcisions
circumference
circumferences
circumflex
circumstance
circumstanced
circumstances
circumstancing
circumstantial
circumvent
circumvented
circumventing
circumvention
circumvents
circus
circuses
cistern
cisterns
citation
citations
cite
cited
cites
cities
citing
citizen
citizens
citizenship
citric
citrus
citruses
city
civic
civics
civil
civilian
civilians
civilities
civility
civilization
civilizations
civilize
civilized
civilizes
civilizing
clack
clacked
clacking
clacks
clad
claim
claimed
claiming
claims
clairvoyance
clairvoyant
clairvoyants
clam
clamber
clambered
clambering
clambers
clammed
clammier
clammiest
clamming
clammy
clamor
clamored
clamoring
clamors
clamp
clamped
clamping
clamps
clams
clan
clandestine
clang
clanged
clanging
clangs
clank
clanked
clanking
clanks
clans
clap
clapped
clapper
clappers
clapping
claps
claptrap
claret
clarification
clarifications
clarified
clarifies
clarify
clarifying
clarinet
clarinets
clarity
clash
clashed
clashes
clashing
clasp
clasped
clasping
clasps
class
classed
classes
classic
classical
classics
classification
classifications
classified
classifies
classify
classifying
classing
classmate
classmates
classroom
classrooms
classy
clatter
clattered
clattering
clatters
clause
clauses
claustrophobia
claw
clawed
clawing
claws
clay
clean
cleaned
cleaner
cleaners
cleanest
cleaning
cleanlier
cleanliest
cleanliness
cleanly
cleans
cleanse
cleansed
cleanser
cleansers
cleanses
cleansing
clear
clearance
clearances
cleared
clearer
clearest
clearing
clearings
clearly
clearness
clears
cleat
cleats
cleavage
cleavages
cleave
cleaved
cleaver
cleavers
cleaves
cleaving
clef
clefs
cleft
clefts
clemency
clench
clenched
clenches
clenching
clergies
clergy
clergyman
clergymen
cleric
clerical
clerics
clerk
clerked
clerking
clerks
clever
cleverer
cleverest
cleverly
cleverness
click
clicked
clicking
clicks
client
clients
cliff
cliffs
climactic
climate
climates
climax
climaxed
climaxes
climaxing
climb
climbed
climber
climbers
climbing
climbs
clime
climes
clinch
clinched
clinches
clinching
cling
clinging
clings
clinic
clinical
clinically
clinics
clink
clinked
clinking
clinks
clip
clipboard
clipboards
clipped
clipping
clippings
clips
clipt
clique
cliques
clitoris
cloak
cloaked
cloaking
cloaks
clock
clocked
clocking
clocks
clockwise
clockwork
clockworks
clod
clods
clog
clogged
clogging
clogs
cloister
cloistered
cloistering
cloisters
clone
clones
close
closed
closely
closeness
closer
closes
closest
closet
closeted
closeting
closets
closing
closure
closures
clot
cloth
clothe
clothed
clothes
clothespin
clothespins
clothing
cloths
clots
clotted
clotting
cloud
cloudburst
cloudbursts
clouded
cloudier
cloudiest
clouding
clouds
cloudy
clout
clouted
clouting
clouts
clove
cloven
clover
clovers
cloves
clown
clowned
clowning
clowns
club
clubbed
clubbing
clubhouse
clubhouses
clubs
cluck
clucked
clucking
clucks
clue
clued
clueing
clueless
clues
cluing
clump
clumped
clumping
clumps
clumsier
clumsiest
clumsily
clumsiness
clumsy
clung
cluster
clustered
clustering
clusters
clutch
clutched
clutches
clutching
clutter
cluttered
cluttering
clutters
coach
coached
coaches
coaching
coagulate
coagulated
coagulates
coagulating
coagulation
coal
coaled
coalesce
coalesced
coalesces
coalescing
coaling
coalition
coalitions
coals
coarse
coarsely
coarsen
coarsened
coarseness
coarsening
coarsens
coarser
coarsest
coast
coastal
coasted
coaster
coasters
coasting
coastline
coastlines
coasts
coat
coated
coating
coats
coax
coaxed
coaxes
coaxing
cob
cobalt
cobble
cobbler
cobblers
cobra
cobras
cobs
cobweb
cobwebs
cocaine
cock
cocked
cockeyed
cockier
cockiest
cocking
cockpit
cockpits
cockroach
cockroaches
cocks
cocktail
cocktails
cocky
cocoa
cocoanut
cocoanuts
cocoas
coconut
coconuts
cocoon
cocooned
cocooning
cocoons
cod
codded
codding
code
coded
codes
coding
cods
coefficient
coefficients
coerce
coerced
coerces
coercing
coercion
coexist
coexisted
coexistence
coexisting
coexists
coffee
coffees
coffer
coffers
coffin
coffined
coffining
coffins
cog
cogency
cogent
cognac
cognacs
cognitive
cogs
coherence
coherent
coherently
coil
coiled
coiling
coils
coin
coinage
coinages
coincide
coincided
coincidence
coincidences
coincidental
coincidentally
coincides
coinciding
coined
coining
coins
coke
coked
cokes
coking
colander
colanders
cold
colder
coldest
coldly
coldness
colds
colic
collaborate
collaborated
collaborates
collaborating
collaboration
collaborations
collaborative
collaborator
collaborators
collage
collages
collapse
collapsed
collapses
collapsible
collapsing
collar
collarbone
collarbones
collared
collaring
collars
collate
collated
collateral
collates
collating
collation
colleague
colleagues
collect
collected
collecting
collection
collections
collective
collectively
collectives
collector
collectors
collects
college
colleges
collegiate
collide
collided
collides
colliding
collie
collies
collision
collisions
colloquial
colloquialism
colloquialisms
collusion
colon
colonel
colonels
colones
colonial
colonials
colonies
colonization
colonize
colonized
colonizes
colonizing
colons
colony
color
colored
coloreds
colorful
coloring
colorless
colors
colossal
colt
colts
column
columns
coma
comas
comb
combat
combatant
combatants
combated
combating
combats
combatted
combatting
combed
combination
combinations
combine
combined
combines
combing
combining
combs
combustible
combustibles
combustion
come
comeback
comedian
comedians
comedies
comedy
comelier
comeliest
comely
comes
comestible
comestibles
comet
comets
comfort
comfortable
comfortably
comforted
comforting
comforts
comic
comical
comics
coming
comings
comma
command
commandant
commandants
commanded
commandeer
commandeered
commandeering
commandeers
commander
commanders
commanding
commandment
commandments
commando
commandoes
commandos
commands
commas
commemorate
commemorated
commemorates
commemorating
commemoration
commemorations
commence
commenced
commencement
commencements
commences
commencing
commend
commendable
commendation
commendations
commended
commending
commends
comment
commentaries
commentary
commentator
commentators
commented
commenting
comments
commerce
commercial
commercialism
commercialize
commercialized
commercializes
commercializing
commercially
commercials
commiserate
commiserated
commiserates
commiserating
commiseration
commiserations
commission
commissioned
commissioner
commissioners
commissioning
commissions
commit
commitment
commitments
commits
committed
committee
committees
committing
commodities
commodity
commodore
commodores
common
commoner
commonest
commonly
commonplace
commonplaces
commons
commonwealth
commonwealths
commotion
commotions
communal
commune
communed
communes
communicable
communicate
communicated
communicates
communicating
communication
communications
communicative
communicator
communing
communion
communions
communique
communiques
communism
communist
communists
communities
community
commutative
commute
commuted
commuter
commuters
commutes
commuting
compact
compacted
compacter
compactest
compacting
compaction
compacts
companies
companion
companions
companionship
company
comparable
comparative
comparatively
comparatives
compare
compared
compares
comparing
comparison
comparisons
compartment
compartments
compass
compassed
compasses
compassing
compassion
compassionate
compatibility
compatible
compatibles
compatriot
compatriots
compel
compelled
compelling
compels
compensate
compensated
compensates
compensating
compensation
compensations
compete
competed
competence
competences
competent
competently
competes
competing
competition
competitions
competitive
competitor
competitors
compilation
compilations
compile
compiled
compiler
compilers
compiles
compiling
complacency
complacent
complain
complained
complaining
complains
complaint
complaints
complement
complementary
complemented
complementing
complements
complete
completed
completely
completeness
completer
completes
completest
completing
completion
complex
complexes
complexion
complexioned
complexions
complexities
complexity
compliance
compliant
complicate
complicated
complicates
complicating
complication
complications
complied
complies
compliment
complimentary
complimented
complimenting
compliments
comply
complying
component
components
compose
composed
composer
composers
composes
composing
composite
composites
composition
compositions
compost
composted
composting
composts
composure
compound
compounded
compounding
compounds
comprehend
comprehended
comprehending
comprehends
comprehensible
comprehension
comprehensions
comprehensive
comprehensively
comprehensives
compress
compressed
compresses
compressing
compression
comprise
comprised
comprises
comprising
compromise
compromised
compromises
compromising
compulsion
compulsions
compulsive
compulsories
compulsory
compunction
compunctions
computation
computational
computations
compute
computed
computer
computerize
computerized
computerizes
computerizing
computers
computes
computing
comrade
comrades
comradeship
con
concatenate
concatenated
concatenates
concatenating
concatenation
concatenations
concave
conceal
concealed
concealing
concealment
conceals
concede
conceded
concedes
conceding
conceit
conceited
conceits
conceivable
conceivably
conceive
conceived
conceives
conceiving
concentrate
concentrated
concentrates
concentrating
concentration
concentrations
concentric
concept
conception
conceptions
concepts
conceptual
conceptually
concern
concerned
concerning
concerns
concert
concerted
concerti
concerting
concerto
concertos
concerts
concession
concessions
conciliate
conciliated
conciliates
conciliating
conciliation
concise
concisely
conciseness
conciser
concisest
conclude
concluded
concludes
concluding
conclusion
conclusions
conclusive
conclusively
concoct
concocted
concocting
concoction
concoctions
concocts
concord
concordance
concourse
concourses
concrete
concreted
concretes
concreting
concur
concurred
concurrence
concurrences
concurrency
concurrent
concurrently
concurring
concurs
concussion
concussions
condemn
condemnation
condemnations
condemned
condemning
condemns
condensation
condensations
condense
condensed
condenses
condensing
condescend
condescended
condescending
condescends
condiment
condiments
condition
conditional
conditionally
conditionals
conditioned
conditioning
conditions
condolence
condolences
condom
condominium
condominiums
condoms
condone
condoned
condones
condoning
condor
condors
conducive
conduct
conducted
conducting
conductor
conductors
conducts
cone
cones
confection
confections
confederacies
confederacy
confederate
confederated
confederates
confederating
confederation
confederations
confer
conference
conferences
conferred
conferrer
conferring
confers
confess
confessed
confesses
confessing
confession
confessions
confetti
confidant
confidants
confide
confided
confidence
confidences
confident
confidential
confidentiality
confidentially
confidently
confides
confiding
configurable
configuration
configurations
configure
configured
configures
configuring
confine
confined
confinement
confinements
confines
confining
confirm
confirmation
confirmations
confirmed
confirming
confirms
confiscate
confiscated
confiscates
confiscating
confiscation
confiscations
conflict
conflicted
conflicting
conflicts
conform
conformed
conforming
conformity
conforms
confound
confounded
confounding
confounds
confront
confrontation
confrontations
confronted
confronting
confronts
confuse
confused
confuses
confusing
confusion
congeal
congealed
congealing
congeals
congenial
congest
congested
congesting
congestion
congests
conglomerate
conglomerated
conglomerates
conglomerating
congratulate
congratulated
congratulates
congratulating
congratulations
congregate
congregated
congregates
congregating
congregation
congregations
congress
congresses
congressman
congressmen
congresswoman
congresswomen
congruent
conical
conifer
coniferous
conifers
conjecture
conjectured
conjectures
conjecturing
conjugal
conjugate
conjugated
conjugates
conjugating
conjugation
conjugations
conjunction
conjunctions
conjure
conjured
conjures
conjuring
connect
connected
connecter
connecters
connecting
connection
connections
connective
connectivity
connector
connectors
connects
conned
conning
connoisseur
connoisseurs
connotation
connotations
connote
connoted
connotes
connoting
conquer
conquered
conquering
conqueror
conquerors
conquers
conquest
conquests
cons
conscience
consciences
conscientious
conscious
consciously
consciousness
consciousnesses
consecrate
consecrated
consecrates
consecrating
consecutive
consensus
consensuses
consent
consented
consenting
consents
consequence
consequences
consequent
consequential
consequently
conservation
conservatism
conservative
conservatives
conservatories
conservatory
conserve
conserved
conserves
conserving
consider
considerable
considerably
considerate
consideration
considerations
considered
considering
considers
consign
consigned
consigning
consignment
consignments
consigns
consist
consisted
consistencies
consistency
consistent
consistently
consisting
consists
consolation
consolations
console
consoled
consoles
consolidate
consolidated
consolidates
consolidating
consolidation
consolidations
consoling
consonant
consonants
consort
consorted
consorting
consortium
consorts
conspicuous
conspicuously
conspiracies
conspiracy
conspirator
conspirators
conspire
conspired
conspires
conspiring
constancy
constant
constantly
constants
constellation
constellations
consternation
constipation
constituencies
constituency
constituent
constituents
constitute
constituted
constitutes
constituting
constitution
constitutional
constitutionally
constitutionals
constitutions
constrain
constrained
constraining
constrains
constraint
constraints
constrict
constricted
constricting
constriction
constrictions
constricts
construct
constructed
constructing
construction
constructions
constructive
constructs
construe
construed
construes
construing
consul
consular
consulate
consulates
consuls
consult
consultancy
consultant
consultants
consultation
consultations
consulted
consulting
consults
consumable
consumables
consume
consumed
consumer
consumerism
consumers
consumes
consuming
consummate
consummated
consummates
consummating
consumption
contact
contacted
contacting
contacts
contagion
contagions
contagious
contain
contained
container
containers
containing
contains
contaminate
contaminated
contaminates
contaminating
contamination
contemplate
contemplated
contemplates
contemplating
contemplation
contemplative
contemplatives
contemporaries
contemporary
contempt
contemptible
contemptuous
contend
contended
contender
contenders
contending
contends
content
contented
contenting
contention
contentions
contentious
contentment
contents
contest
contestant
contestants
contested
contesting
contests
context
contexts
contextual
contiguous
continent
continental
continentals
continents
contingencies
contingency
contingent
contingents
continual
continually
continuation
continuations
continue
continued
continues
continuing
continuity
continuous
continuously
continuum
contort
contorted
contorting
contortion
contortions
contorts
contour
contoured
contouring
contours
contraband
contraception
contraceptive
contraceptives
contract
contracted
contracting
contraction
contractions
contractor
contractors
contracts
contractual
contradict
contradicted
contradicting
contradiction
contradictions
contradictory
contradicts
contraption
contraptions
contraries
contrary
contrast
contrasted
contrasting
contrasts
contravene
contravenes
contravention
contribute
contributed
contributes
contributing
contribution
contributions
contributor
contributors
contributory
contrite
contrive
contrived
contrives
contriving
control
controllable
controlled
controller
controllers
controlling
controls
controversial
controversies
controversy
convalesce
convalesced
convalescence
convalescences
convalescent
convalescents
convalesces
convalescing
convection
convene
convened
convenes
convenience
conveniences
convenient
conveniently
convening
convent
convention
conventional
conventionally
conventions
convents
converge
converged
convergence
converges
converging
conversant
conversation
conversational
conversations
converse
conversed
conversely
converses
conversing
conversion
conversions
convert
converted
converter
converters
convertible
convertibles
converting
convertor
convertors
converts
convex
convey
conveyance
conveyances
conveyed
conveying
conveys
convict
convicted
convicting
conviction
convictions
convicts
convince
convinced
convinces
convincing
convincingly
convoluted
convoy
convoyed
convoying
convoys
convulse
convulsed
convulses
convulsing
convulsion
convulsions
convulsive
coo
cooed
cooing
cook
cookbook
cookbooks
cooked
cooker
cookie
cookies
cooking
cooks
cooky
cool
cooled
cooler
coolers
coolest
cooling
coolly
cools
coop
cooped
cooper
cooperate
cooperated
cooperates
cooperating
cooperation
cooperative
cooperatives
cooping
coops
coordinate
coordinated
coordinates
coordinating
coordination
coordinator
coos
cop
cope
coped
copes
copied
copier
copiers
copies
coping
copious
copiously
copped
copper
copperhead
copperheads
coppers
copping
cops
copulate
copulation
copy
copying
copyright
copyrighted
copyrighting
copyrights
coral
corals
cord
corded
cordial
cordially
cordials
cording
cordless
cordon
cordoned
cordoning
cordons
cords
corduroy
core
cored
cores
coring
cork
corked
corking
corks
corkscrew
corkscrewed
corkscrewing
corkscrews
corn
cornea
corneas
corned
corner
cornered
cornering
corners
cornet
cornets
cornflakes
cornier
corniest
corning
cornmeal
corns
cornstarch
corny
corollary
coronaries
coronary
coronation
coronations
coroner
coroners
corporal
corporals
corporate
corporation
corporations
corps
corpse
corpses
corpulent
corpus
corpuscle
corpuscles
corral
corralled
corralling
corrals
correct
corrected
correcter
correctest
correcting
correction
corrections
corrective
correctly
correctness
corrector
corrects
correlate
correlated
correlates
correlating
correlation
correlations
correspond
corresponded
correspondence
correspondences
correspondent
correspondents
corresponding
correspondingly
corresponds
corridor
corridors
corroborate
corroborated
corroborates
corroborating
corroboration
corrode
corroded
corrodes
corroding
corrosion
corrosive
corrosives
corrupt
corrupted
corrupter
corruptest
corruptible
corrupting
corruption
corruptions
corrupts
corsage
corsages
corset
corseted
corseting
corsets
cortex
cosier
cosies
cosiest
cosmetic
cosmetics
cosmic
cosmology
cosmonaut
cosmonauts
cosmopolitan
cosmopolitans
cosmos
cosmoses
cost
costed
costing
costings
costlier
costliest
costly
costs
costume
costumed
costumes
costuming
cosy
cot
cots
cottage
cottages
cotton
cottoned
cottoning
cottons
cottontail
cottontails
cottonwood
cottonwoods
couch
couched
couches
couching
cougar
cougars
cough
coughed
coughing
coughs
could
council
councillor
councillors
councilor
councilors
councils
counsel
counseled
counseling
counselled
counsellor
counsellors
counselor
counselors
counsels
count
countable
countdown
countdowns
counted
countenance
countenanced
countenances
countenancing
counter
counteract
counteracted
counteracting
counteracts
counterattack
counterattacked
counterattacking
counterattacks
counterbalance
counterbalanced
counterbalances
counterbalancing
counterclockwise
countered
counterexample
counterfeit
counterfeited
counterfeiting
counterfeits
countering
counterpart
counterparts
counters
countersign
countersigned
countersigning
countersigns
countess
countesses
counties
counting
countless
countries
country
countryman
countrymen
countryside
countrysides
counts
county
coup
couple
coupled
couples
coupling
coupon
coupons
coups
courage
courageous
courageously
courier
couriers
course
coursed
courser
courses
coursing
court
courted
courteous
courteously
courtesies
courtesy
courthouse
courthouses
courting
courtroom
courtrooms
courts
courtship
courtships
courtyard
courtyards
cousin
cousins
cove
covenant
covenanted
covenanting
covenants
cover
coverage
covered
covering
covers
covert
covertly
coverts
coves
covet
coveted
coveting
covetous
covets
cow
coward
cowardice
cowardly
cowards
cowboy
cowboys
cowed
cower
cowered
cowering
cowers
cowgirl
cowgirls
cowhide
cowhides
cowing
cows
cox
coy
coyer
coyest
coyote
coyotes
cozier
cozies
coziest
cozily
coziness
cozy
crab
crabbed
crabbier
crabbiest
crabbing
crabby
crabs
crack
cracked
cracker
crackers
cracking
crackle
crackled
crackles
crackling
crackpot
crackpots
cracks
cradle
cradled
cradles
cradling
craft
crafted
craftier
craftiest
craftily
crafting
crafts
craftsman
craftsmen
crafty
crag
craggier
craggiest
craggy
crags
cram
crammed
cramming
cramp
cramped
cramping
cramps
crams
cranberries
cranberry
crane
craned
cranes
crania
craning
cranium
craniums
crank
cranked
crankier
crankiest
cranking
cranks
cranky
crap
crash
crashed
crashes
crashing
crass
crasser
crassest
crate
crated
crater
cratered
cratering
craters
crates
crating
crave
craved
craves
craving
cravings
crawfish
crawfishes
crawl
crawled
crawling
crawls
crayfish
crayfishes
crayon
crayoned
crayoning
crayons
craze
crazed
crazes
crazier
crazies
craziest
crazily
craziness
crazing
crazy
creak
creaked
creakier
creakiest
creaking
creaks
creaky
cream
creamed
creamier
creamiest
creaming
creams
creamy
crease
creased
creases
creasing
create
created
creates
creating
creation
creations
creative
creatively
creatives
creativity
creator
creators
creature
creatures
credence
credential
credentials
credibility
credible
credit
creditable
credited
crediting
creditor
creditors
credits
credulous
creed
creeds
creek
creeks
creep
creepier
creepiest
creeping
creeps
creepy
cremate
cremated
cremates
cremating
cremation
cremations
crepe
crepes
crept
crescendi
crescendo
crescendos
crescent
crescents
crest
crested
crestfallen
cresting
crests
cretin
cretinous
cretins
crevasse
crevasses
crevice
crevices
crew
crewed
crewing
crews
crib
cribbed
cribbing
cribs
cricket
crickets
cried
cries
crime
crimes
criminal
criminally
criminals
crimson
crimsoned
crimsoning
crimsons
cringe
cringed
cringes
cringing
crinkle
crinkled
crinkles
crinkling
cripple
crippled
cripples
crippling
crises
crisis
crisp
crisped
crisper
crispest
crisping
crisply
crisps
crispy
crisscross
crisscrossed
crisscrosses
crisscrossing
criteria
criterion
criterions
critic
critical
critically
criticism
criticisms
criticize
criticized
criticizes
criticizing
critics
critique
critiqued
critiques
critiquing
croak
croaked
croaking
croaks
crochet
crocheted
crocheting
crochets
croci
crock
crockery
crocks
crocodile
crocodiles
crocus
crocuses
crofts
cronies
crony
crook
crooked
crookeder
crookedest
crooking
crooks
croon
crooned
crooning
croons
crop
cropped
cropping
crops
croquet
cross
crossbow
crossbows
crossed
crosser
crosses
crossest
crossing
crossings
crossroad
crossroads
crosswalk
crosswalks
crossword
crosswords
crotch
crotches
crouch
crouched
crouches
crouching
crow
crowbar
crowbars
crowd
crowded
crowding
crowds
crowed
crowing
crown
crowned
crowning
crowns
crows
crucial
crucially
crucified
crucifies
crucifix
crucifixes
crucifixion
crucifixions
crucify
crucifying
crude
crudely
cruder
crudest
crudity
cruel
crueler
cruelest
crueller
cruellest
cruelly
cruelties
cruelty
cruise
cruised
cruiser
cruisers
cruises
cruising
crumb
crumbed
crumbing
crumble
crumbled
crumbles
crumblier
crumbliest
crumbling
crumbly
crumbs
crummier
crummiest
crummy
crumple
crumpled
crumples
crumpling
crunch
crunched
crunches
crunching
crunchy
crusade
crusaded
crusader
crusaders
crusades
crusading
crush
crushed
crushes
crushing
crust
crustacean
crustaceans
crusted
crustier
crustiest
crusting
crusts
crusty
crutch
crutches
crux
cruxes
cry
crybabies
crybaby
crying
crypt
cryptic
crypts
crystal
crystalize
crystalized
crystalizes
crystalizing
crystallization
crystallize
crystallized
crystallizes
crystallizing
crystals
cs
cub
cube
cubed
cubes
cubic
cubicle
cubicles
cubing
cubs
cuckoo
cuckoos
cucumber
cucumbers
cuddle
cuddled
cuddles
cuddling
cuddly
cue
cued
cueing
cues
cuff
cuffed
cuffing
cuffs
cuing
cuisine
cuisines
culinary
cull
culled
cullender
cullenders
culling
culls
culminate
culminated
culminates
culminating
culmination
culminations
culpable
culprit
culprits
cult
cultivate
cultivated
cultivates
cultivating
cultivation
cults
cultural
culturally
culture
cultured
cultures
culturing
cumbersome
cumming
cums
cumulative
cunning
cunninger
cunningest
cunningly
cup
cupboard
cupboards
cupful
cupfuls
cupped
cupping
cups
cupsful
cur
curable
curator
curators
curb
curbed
curbing
curbs
curd
curdle
curdled
curdles
curdling
curds
cure
cured
cures
curfew
curfews
curing
curio
curios
curiosities
curiosity
curious
curiously
curl
curled
curling
curls
curly
currant
currants
currencies
currency
current
currently
currents
curricula
curriculum
curriculums
curried
curries
curry
currying
curse
cursed
curses
cursing
cursor
cursory
curst
curt
curtail
curtailed
curtailing
curtails
curtain
curtained
curtaining
curtains
curter
curtest
curtsey
curtseyed
curtseying
curtseys
curtsied
curtsies
curtsy
curtsying
curvature
curvatures
curve
curved
curves
curving
cushion
cushioned
cushioning
cushions
custard
custards
custodian
custodians
custody
custom
customary
customer
customers
customization
customize
customized
customizes
customizing
customs
cut
cutback
cutbacks
cute
cuter
cutest
cuticle
cuticles
cutlery
cutlet
cutlets
cuts
cutter
cutters
cutthroat
cutthroats
cutting
cuttings
cyanide
cybernetics
cycle
cycled
cycles
cyclic
cycling
cyclist
cyclists
cyclone
cyclones
cylinder
cylinders
cylindrical
cymbal
cymbals
cynic
cynical
cynicism
cynics
cypher
cypress
cypresses
cyst
cysts
czar
czars
dab
dabbed
dabbing
dabble
dabbled
dabbles
dabbling
dabs
dachshund
dachshunds
dad
daddies
daddy
dads
daemon
daffodil
daffodils
daft
dagger
daggers
dailies
daily
daintier
dainties
daintiest
daintily
dainty
dairies
dairy
dais
daises
daisies
daisy
dallied
dallies
dally
dallying
dam
damage
damaged
damages
damaging
dame
dames
dammed
damming
damn
damnation
damndest
damned
damnedest
damning
damns
damp
damped
dampen
dampened
dampening
dampens
damper
dampest
damping
dampness
damps
dams
damsel
damsels
dance
danced
dancer
dancers
dances
dancing
dandelion
dandelions
dandier
dandies
dandiest
dandruff
dandy
danger
dangerous
dangerously
dangers
dangle
dangled
dangles
dangling
dank
danker
dankest
dapper
dapperer
dapperest
dare
dared
daredevil
daredevils
dares
daring
dark
darken
darkened
darkening
darkens
darker
darkest
darkly
darkness
darling
darlings
darn
darned
darning
darns
dart
darted
darting
darts
dash
dashboard
dashboards
dashed
dashes
dashing
dastardly
data
database
databases
date
dated
dates
dating
datum
daub
daubed
daubing
daubs
daughter
daughters
daunt
daunted
daunting
dauntless
daunts
dawdle
dawdled
dawdles
dawdling
dawn
dawned
dawning
dawns
day
daybreak
daydream
daydreamed
daydreaming
daydreams
daydreamt
daylight
days
daytime
daze
dazed
dazes
dazing
dazzle
dazzled
dazzles
dazzling
deacon
deacons
dead
deaden
deadened
deadening
deadens
deader
deadest
deadlier
deadliest
deadline
deadlines
deadlock
deadlocked
deadlocking
deadlocks
deadly
deaf
deafer
deafest
deafness
deal
dealer
dealers
dealing
dealings
deals
dealt
dean
deans
dear
dearer
dearest
dearly
dears
dearth
dearths
death
deathbed
deathbeds
deaths
deaves
debase
debased
debasement
debasements
debases
debasing
debatable
debate
debated
debates
debating
debaucheries
debauchery
debilitate
debilitated
debilitates
debilitating
debilities
debility
debit
debited
debiting
debits
debonair
debrief
debriefed
debriefing
debriefs
debris
debt
debtor
debtors
debts
debug
debugged
debugger
debugging
debugs
debunk
debunked
debunking
debunks
debut
debuted
debuting
debuts
decade
decadence
decadent
decadents
decades
decanter
decanters
decapitate
decapitated
decapitates
decapitating
decay
decayed
decaying
decays
decease
deceased
deceases
deceasing
deceit
deceitful
deceitfully
deceits
deceive
deceived
deceives
deceiving
decencies
decency
decent
decently
decentralization
decentralize
decentralized
decentralizes
decentralizing
deception
deceptions
deceptive
decibel
decibels
decide
decided
decidedly
decides
deciding
deciduous
decimal
decimals
decimate
decimated
decimates
decimating
decipher
deciphered
deciphering
deciphers
decision
decisions
decisive
decisively
deck
decked
decking
decks
declaration
declarations
declare
declared
declares
declaring
declension
decline
declined
declines
declining
decode
decoded
decoder
decodes
decoding
decompose
decomposed
decomposes
decomposing
decomposition
decorate
decorated
decorates
decorating
decoration
decorations
decorative
decorator
decorators
decorous
decorum
decoy
decoyed
decoying
decoys
decrease
decreased
decreases
decreasing
decree
decreed
decreeing
decrees
decrepit
decried
decries
decry
decrying
dedicate
dedicated
dedicates
dedicating
dedication
dedications
deduce
deduced
deduces
deducing
deduct
deducted
deducting
deduction
deductions
deductive
deducts
deed
deeded
deeding
deeds
deem
deemed
deeming
deems
deep
deepen
deepened
deepening
deepens
deeper
deepest
deeply
deeps
deer
deers
deface
defaced
defaces
defacing
defamation
defamatory
defame
defamed
defames
defaming
default
defaulted
defaulting
defaults
defeat
defeated
defeating
defeatist
defeats
defecate
defecated
defecates
defecating
defect
defected
defecting
defective
defectives
defects
defend
defendant
defendants
defended
defender
defenders
defending
defends
defense
defensed
defenseless
defenses
defensible
defensing
defensive
defer
deference
deferential
deferred
deferring
defers
defiance
defiant
defiantly
deficiencies
deficiency
deficient
deficit
deficits
defied
defies
defile
defiled
defiles
defiling
definable
define
defined
defines
defining
definite
definitely
definition
definitions
definitive
deflate
deflated
deflates
deflating
deflation
deflect
deflected
deflecting
deflection
deflections
deflects
deform
deformed
deforming
deformities
deformity
deforms
defraud
defrauded
defrauding
defrauds
defrost
defrosted
defrosting
defrosts
deft
defter
deftest
deftly
defunct
defy
defying
degenerate
degenerated
degenerates
degenerating
degradation
degrade
degraded
degrades
degrading
degree
degrees
dehydrate
dehydrated
dehydrates
dehydrating
deified
deifies
deify
deifying
deign
deigned
deigning
deigns
deities
deity
deject
dejected
dejecting
dejection
dejects
delay
delayed
delaying
delays
delectable
delegate
delegated
delegates
delegating
delegation
delegations
delete
deleted
deleterious
deletes
deleting
deletion
deletions
deli
deliberate
deliberated
deliberately
deliberates
deliberating
deliberation
deliberations
delicacies
delicacy
delicate
delicately
delicatessen
delicatessens
delicious
deliciously
delight
delighted
delightful
delighting
delights
delimit
delimited
delimiter
delimiters
delimiting
delimits
delinquencies
delinquency
delinquent
delinquents
deliria
delirious
deliriously
delirium
deliriums
delis
deliver
deliverance
delivered
deliveries
delivering
delivers
delivery
delta
deltas
delude
deluded
deludes
deluding
deluge
deluged
deluges
deluging
delusion
delusions
deluxe
delve
delved
delves
delving
demagog
demagogs
demagogue
demagogues
demand
demanded
demanding
demands
demean
demeaned
demeaning
demeanor
demeans
demented
dementia
demerit
demerits
demise
demised
demises
demising
democracies
democracy
democrat
democratic
democratically
democrats
demolish
demolished
demolishes
demolishing
demolition
demolitions
demon
demons
demonstrably
demonstrate
demonstrated
demonstrates
demonstrating
demonstration
demonstrations
demonstrative
demonstratives
demonstrator
demonstrators
demoralize
demoralized
demoralizes
demoralizing
demote
demoted
demotes
demoting
demotion
demotions
demount
demure
demurely
demurer
demurest
den
denial
denials
denied
denies
denigrate
denim
denims
denomination
denominations
denominator
denominators
denote
denoted
denotes
denoting
denounce
denounced
denounces
denouncing
dens
dense
densely
denser
densest
densities
density
dent
dental
dented
denting
dentist
dentistry
dentists
dents
denunciation
denunciations
deny
denying
deodorant
deodorants
deodorize
deodorized
deodorizes
deodorizing
depart
departed
departing
department
departmental
departments
departs
departure
departures
depend
dependable
dependance
dependant
dependants
depended
dependence
dependencies
dependency
dependent
dependents
depending
depends
depict
depicted
depicting
depiction
depicts
deplete
depleted
depletes
depleting
deplorable
deplore
deplored
deplores
deploring
deport
deportation
deportations
deported
deporting
deportment
deports
depose
deposed
deposes
deposing
deposit
deposited
depositing
deposits
depot
depots
deprave
depraved
depraves
depraving
depravities
depravity
deprecate
deprecated
deprecates
deprecating
depreciate
depreciated
depreciates
depreciating
depreciation
depress
depressed
depresses
depressing
depressingly
depression
depressions
deprivation
deprivations
deprive
deprived
deprives
depriving
depth
depths
deputies
deputy
derail
derailed
derailing
derailment
derailments
derails
derange
deranged
deranges
deranging
derelict
derelicts
deride
derided
derides
deriding
derision
derivation
derivations
derivative
derivatives
derive
derived
derives
deriving
derogatory
derrick
derricks
descend
descendant
descendants
descended
descendent
descendents
descending
descends
descent
descents
describable
describe
described
describes
describing
description
descriptions
descriptive
descriptor
descriptors
desecrate
desecrated
desecrates
desecrating
desecration
desegregation
desert
deserted
deserter
deserters
deserting
deserts
deserve
deserved
deserves
deserving
design
designate
designated
designates
designating
designation
designations
designed
designer
designers
designing
designs
desirability
desirable
desire
desired
desires
desiring
desirous
desist
desisted
desisting
desists
desk
desks
desktop
desolate
desolated
desolates
desolating
desolation
despair
despaired
despairing
despairs
despatch
despatched
despatches
despatching
desperate
desperately
desperation
despicable
despise
despised
despises
despising
despite
despondent
despot
despotic
despots
dessert
desserts
destabilize
destination
destinations
destine
destined
destines
destinies
destining
destiny
destitute
destitution
destroy
destroyed
destroyer
destroyers
destroying
destroys
destruction
destructive
detach
detachable
detached
detaches
detaching
detachment
detachments
detail
detailed
detailing
details
detain
detained
detaining
detains
detect
detectable
detected
detecting
detection
detective
detectives
detector
detectors
detects
detention
detentions
deter
detergent
detergents
deteriorate
deteriorated
deteriorates
deteriorating
deterioration
determinable
determination
determinations
determine
determined
determines
determining
determinism
deterministic
deterred
deterrent
deterrents
deterring
deters
detest
detested
detesting
detests
dethrone
dethroned
dethrones
dethroning
detonate
detonated
detonates
detonating
detonation
detonations
detonator
detonators
detour
detoured
detouring
detours
detract
detracted
detracting
detracts
detriment
detrimental
detriments
devalue
devastate
devastated
devastates
devastating
devastation
develop
developed
developer
developers
developing
development
developments
develops
deviant
deviate
deviated
deviates
deviating
deviation
deviations
device
devices
devil
deviled
deviling
devilled
devilling
devils
devious
devise
devised
devises
devising
devoid
devolution
devolve
devolved
devolves
devolving
devote
devoted
devotee
devotees
devotes
devoting
devotion
devotions
devour
devoured
devouring
devours
devout
devouter
devoutest
devoutly
dew
dexterity
dexterous
dextrous
diabetes
diabetic
diabetics
diabolical
diagnose
diagnosed
diagnoses
diagnosing
diagnosis
diagnostic
diagnostics
diagonal
diagonally
diagonals
diagram
diagramed
diagraming
diagrammed
diagramming
diagrams
dial
dialect
dialects
dialed
dialing
dialings
dialog
dialogs
dialogue
dialogues
dials
diameter
diameters
diametrically
diamond
diamonds
diaper
diapered
diapering
diapers
diaphragm
diaphragms
diaries
diarrhea
diarrhoea
diary
diatribe
dice
diced
dices
dicing
dictate
dictated
dictates
dictating
dictation
dictations
dictator
dictatorial
dictators
dictatorship
dictatorships
diction
dictionaries
dictionary
did
die
died
dies
diesel
dieseled
dieseling
diesels
diet
dietaries
dietary
dieted
dieting
diets
differ
differed
difference
differences
different
differential
differentiate
differentiated
differentiates
differentiating
differentiation
differently
differing
differs
difficult
difficulties
difficulty
diffuse
diffused
diffuses
diffusing
diffusion
dig
digest
digested
digestible
digesting
digestion
digestions
digestive
digests
digging
digit
digital
digitally
digitize
digitized
digitizes
digitizing
digits
dignified
dignifies
dignify
dignifying
dignitaries
dignitary
dignities
dignity
digress
digressed
digresses
digressing
digression
digressions
digs
dike
diked
dikes
diking
dilapidated
dilate
dilated
dilates
dilating
dilation
dilemma
dilemmas
diligence
diligent
diligently
dill
dills
dilute
diluted
dilutes
diluting
dilution
dim
dime
dimension
dimensional
dimensions
dimer
dimes
diminish
diminished
diminishes
diminishing
diminutive
diminutives
dimly
dimmed
dimmer
dimmest
dimming
dimple
dimpled
dimples
dimpling
dims
din
dine
dined
diner
diners
dines
dinghies
dinghy
dingier
dingiest
dingy
dining
dinned
dinner
dinnered
dinnering
dinners
dinning
dinosaur
dinosaurs
dins
diocese
dioceses
dioxide
dip
diphtheria
diphthong
diphthongs
diploma
diplomacy
diplomas
diplomat
diplomata
diplomatic
diplomatically
diplomats
dipped
dipping
dips
dire
direct
directed
directer
directest
directing
direction
directions
directive
directives
directly
directness
director
directories
directors
directory
directs
direr
direst
dirge
dirges
dirt
dirtied
dirtier
dirties
dirtiest
dirty
dirtying
disabilities
disability
disable
disabled
disables
disabling
disadvantage
disadvantaged
disadvantageous
disadvantages
disadvantaging
disagree
disagreeable
disagreeably
disagreed
disagreeing
disagreement
disagreements
disagrees
disallow
disallowed
disallowing
disallows
disambiguate
disappear
disappearance
disappearances
disappeared
disappearing
disappears
disappoint
disappointed
disappointing
disappointment
disappointments
disappoints
disapproval
disapprove
disapproved
disapproves
disapproving
disarm
disarmament
disarmed
disarming
disarms
disarray
disarrayed
disarraying
disarrays
disaster
disasters
disastrous
disavow
disavowed
disavowing
disavows
disband
disbanded
disbanding
disbands
disbelief
disbelieve
disbelieved
disbelieves
disbelieving
disburse
disbursed
disbursement
disbursements
disburses
disbursing
disc
discard
discarded
discarding
discards
discern
discerned
discernible
discerning
discerns
discharge
discharged
discharges
discharging
disciple
disciples
disciplinarian
disciplinarians
disciplinary
discipline
disciplined
disciplines
disciplining
disclaim
disclaimed
disclaimer
disclaiming
disclaims
disclose
disclosed
discloses
disclosing
disclosure
disclosures
disco
discolor
discoloration
discolorations
discolored
discoloring
discolors
discomfort
discomforted
discomforting
discomforts
disconcert
disconcerted
disconcerting
disconcerts
disconnect
disconnected
disconnecting
disconnects
disconsolate
disconsolately
discontent
discontented
discontenting
discontents
discontinue
discontinued
discontinues
discontinuing
discontinuity
discord
discordant
discorded
discording
discords
discos
discount
discounted
discounting
discounts
discourage
discouraged
discouragement
discouragements
discourages
discouraging
discourse
discoursed
discourses
discoursing
discourteous
discourtesies
discourtesy
discover
discovered
discoveries
discovering
discovers
discovery
discredit
discredited
discrediting
discredits
discreet
discreeter
discreetest
discreetly
discrepancies
discrepancy
discrete
discretion
discretionary
discriminate
discriminated
discriminates
discriminating
discrimination
discriminatory
discs
discus
discuses
discuss
discussed
discusses
discussing
discussion
discussions
disdain
disdained
disdainful
disdaining
disdains
disease
diseased
diseases
disembark
disembarkation
disembarked
disembarking
disembarks
disenchantment
disengage
disengaged
disengages
disengaging
disentangle
disentangled
disentangles
disentangling
disfavor
disfavored
disfavoring
disfavors
disfigure
disfigured
disfigures
disfiguring
disgrace
disgraced
disgraceful
disgraces
disgracing
disgruntle
disgruntled
disgruntles
disgruntling
disguise
disguised
disguises
disguising
disgust
disgusted
disgusting
disgustingly
disgusts
dish
dishearten
disheartened
disheartening
disheartens
dished
dishes
dishing
dishonest
dishonestly
dishonesty
dishonor
dishonorable
dishonored
dishonoring
dishonors
dishwasher
dishwashers
disillusion
disillusioned
disillusioning
disillusionment
disillusions
disincentive
disinfect
disinfectant
disinfectants
disinfected
disinfecting
disinfects
disingenuous
disinherit
disinherited
disinheriting
disinherits
disintegrate
disintegrated
disintegrates
disintegrating
disintegration
disinterested
disjoint
disjointed
disjointing
disjoints
disk
disks
dislike
disliked
dislikes
disliking
dislocate
dislocated
dislocates
dislocating
dislocation
dislocations
dislodge
dislodged
dislodges
dislodging
disloyal
disloyalty
dismal
dismally
dismantle
dismantled
dismantles
dismantling
dismay
dismayed
dismaying
dismays
dismember
dismembered
dismembering
dismembers
dismiss
dismissal
dismissals
dismissed
dismisses
dismissing
dismissive
dismount
dismounted
dismounting
dismounts
disobedience
disobedient
disobey
disobeyed
disobeying
disobeys
disorder
disordered
disordering
disorderly
disorders
disown
disowned
disowning
disowns
disparage
disparaged
disparages
disparaging
disparate
disparities
disparity
dispassionate
dispassionately
dispatch
dispatched
dispatches
dispatching
dispel
dispelled
dispelling
dispels
dispensaries
dispensary
dispensation
dispensations
dispense
dispensed
dispenser
dispensers
dispenses
dispensing
dispersal
disperse
dispersed
disperses
dispersing
dispersion
displace
displaced
displacement
displacements
displaces
displacing
display
displayed
displaying
displays
displease
displeased
displeases
displeasing
displeasure
disposable
disposables
disposal
disposals
dispose
disposed
disposes
disposing
disposition
dispositions
dispossess
dispossessed
dispossesses
dispossessing
disproportionate
disprove
disproved
disproven
disproves
disproving
dispute
disputed
disputes
disputing
disqualified
disqualifies
disqualify
disqualifying
disquiet
disquieted
disquieting
disquiets
disregard
disregarded
disregarding
disregards
disrepair
disreputable
disrepute
disrespect
disrespected
disrespectful
disrespecting
disrespects
disrupt
disrupted
disrupting
disruption
disruptions
disruptive
disrupts
dissatisfaction
dissatisfied
dissatisfies
dissatisfy
dissatisfying
dissect
dissected
dissecting
dissection
dissections
dissects
disseminate
disseminated
disseminates
disseminating
dissemination
dissension
dissensions
dissent
dissented
dissenter
dissenters
dissenting
dissents
dissertation
dissertations
disservice
disservices
dissident
dissidents
dissimilar
dissimilarities
dissimilarity
dissipate
dissipated
dissipates
dissipating
dissipation
dissociate
dissociated
dissociates
dissociating
dissociation
dissolute
dissolution
dissolve
dissolved
dissolves
dissolving
dissonance
dissonances
dissuade
dissuaded
dissuades
dissuading
distance
distanced
distances
distancing
distant
distantly
distaste
distasteful
distastes
distend
distended
distending
distends
distil
distill
distillation
distillations
distilled
distiller
distilleries
distillers
distillery
distilling
distills
distils
distinct
distincter
distinctest
distinction
distinctions
distinctive
distinctively
distinctly
distinguish
distinguishable
distinguished
distinguishes
distinguishing
distort
distorted
distorter
distorting
distortion
distortions
distorts
distract
distracted
distracting
distraction
distractions
distracts
distraught
distress
distressed
distresses
distressing
distressingly
distribute
distributed
distributes
distributing
distribution
distributions
distributor
distributors
district
districts
distrust
distrusted
distrustful
distrusting
distrusts
disturb
disturbance
disturbances
disturbed
disturbing
disturbs
disuse
disused
disuses
disusing
ditch
ditched
ditches
ditching
dither
dithered
dithering
dithers
ditties
ditto
dittoed
dittoes
dittoing
dittos
ditty
dive
dived
diver
diverge
diverged
divergence
divergences
divergent
diverges
diverging
divers
diverse
diversified
diversifies
diversify
diversifying
diversion
diversions
diversities
diversity
divert
diverted
diverting
diverts
dives
divest
divested
divesting
divests
divide
divided
dividend
dividends
divides
dividing
divine
divined
diviner
divines
divinest
diving
divining
divinities
divinity
divisible
division
divisions
divisive
divisor
divisors
divorce
divorced
divorces
divorcing
divulge
divulged
divulges
divulging
dizzied
dizzier
dizzies
dizziest
dizziness
dizzy
dizzying
do
docile
dock
docked
docking
docks
doctor
doctorate
doctored
doctoring
doctors
doctrine
doctrines
document
documentaries
documentary
documentation
documented
documenting
documents
dodge
dodged
dodges
dodging
dodo
doe
doer
doers
does
dog
dogged
doggedly
doggerel
dogging
doghouse
doghouses
dogma
dogmas
dogmata
dogmatic
dogs
dogwood
dogwoods
doilies
doily
doing
doldrums
dole
doled
doleful
dolefully
doles
doling
doll
dollar
dollars
dolled
dollies
dolling
dolls
dolly
dolphin
dolphins
domain
domains
dome
domed
domes
domestic
domesticate
domesticated
domesticates
domesticating
domesticity
domestics
domicile
domiciled
domiciles
domiciling
dominance
dominant
dominants
dominate
dominated
dominates
dominating
domination
doming
dominion
dominions
domino
dominoes
dominos
don
donate
donated
donates
donating
donation
donations
done
donkey
donkeys
donor
donors
dons
donut
donuts
doodle
doodled
doodles
doodling
doom
doomed
dooming
dooms
door
doorman
doormen
doors
doorstep
doorsteps
doorway
doorways
dope
doped
dopes
dopey
dopier
dopiest
doping
dopy
dormant
dormitories
dormitory
dorsal
dos
dose
dosed
doses
dosing
dot
dote
doted
dotes
doting
dots
dotted
dotting
double
doubled
doubles
doubling
doubly
doubt
doubted
doubtful
doubtfully
doubting
doubtless
doubts
dough
doughnut
doughnuts
dour
dourer
dourest
douse
doused
douses
dousing
dove
doves
dowdier
dowdies
dowdiest
dowdy
down
downcast
downed
downfall
downfalls
downgrade
downgraded
downgrades
downgrading
downhearted
downhill
downhills
downier
downiest
downing
downpour
downpours
downright
downs
downstairs
downstream
downtown
downward
downwards
downy
dowries
dowry
doze
dozed
dozen
dozens
dozes
dozing
drab
drabber
drabbest
drabs
draconian
draft
drafted
draftier
draftiest
drafting
drafts
draftsman
draftsmen
drafty
drag
dragged
dragging
dragon
dragonflies
dragonfly
dragons
drags
drain
drainage
drained
draining
drains
drama
dramas
dramatic
dramatically
dramatist
dramatists
dramatization
dramatizations
dramatize
dramatized
dramatizes
dramatizing
drank
drape
draped
draperies
drapery
drapes
draping
drastic
drastically
draw
drawback
drawbacks
drawbridge
drawbridges
drawer
drawers
drawing
drawings
drawl
drawled
drawling
drawls
drawn
draws
dread
dreaded
dreadful
dreadfully
dreading
dreads
dream
dreamed
dreamer
dreamers
dreamier
dreamiest
dreaming
dreams
dreamy
drearier
dreariest
dreary
dredge
dredged
dredges
dredging
dregs
drench
drenched
drenches
drenching
dress
dressed
dresser
dressers
dresses
dressier
dressiest
dressing
dressings
dressmaker
dressmakers
dressy
drew
dribble
dribbled
dribbles
dribbling
dried
drier
driers
dries
driest
drift
drifted
drifting
drifts
driftwood
drill
drilled
drilling
drills
drily
drink
drinkable
drinker
drinkers
drinking
drinks
drip
dripped
dripping
drips
drive
drivel
driveled
driveling
drivelled
drivelling
drivels
driven
driver
drivers
drives
driveway
driveways
driving
drizzle
drizzled
drizzles
drizzling
droll
droller
drollest
drone
droned
drones
droning
drool
drooled
drooling
drools
droop
drooped
drooping
droops
drop
dropout
dropouts
dropped
dropping
droppings
drops
dross
drought
droughts
drouth
drouthes
drouths
drove
droves
drown
drowned
drowning
drowns
drowse
drowsed
drowses
drowsier
drowsiest
drowsiness
drowsing
drowsy
drudge
drudged
drudgery
drudges
drudging
drug
drugged
drugging
druggist
druggists
drugs
drugstore
drugstores
drum
drummed
drummer
drummers
drumming
drums
drumstick
drumsticks
drunk
drunkard
drunkards
drunken
drunkenly
drunkenness
drunker
drunkest
drunks
dry
dryer
dryers
dryest
drying
dryly
dryness
drys
dual
dualism
dub
dubbed
dubbing
dubious
dubiously
dubs
duchess
duchesses
duck
ducked
ducking
duckling
ducklings
ducks
duct
ducts
dud
dude
duded
dudes
duding
duds
due
duel
dueled
dueling
duelled
duelling
duels
dues
duet
duets
duff
dug
dugout
dugouts
duke
dukes
dull
dulled
duller
dullest
dulling
dullness
dulls
dully
dulness
duly
dumb
dumbbell
dumbbells
dumber
dumbest
dumbfound
dumbfounded
dumbfounding
dumbfounds
dumfound
dumfounded
dumfounding
dumfounds
dummies
dummy
dump
dumped
dumpier
dumpiest
dumping
dumpling
dumplings
dumps
dumpster
dumpy
dunce
dunces
dune
dunes
dung
dunged
dungeon
dungeons
dunging
dungs
dunk
dunked
dunking
dunks
dunno
duo
dupe
duped
dupes
duping
duplex
duplexes
duplicate
duplicated
duplicates
duplicating
duplication
duplicity
durability
durable
duration
duress
during
dusk
duskier
duskiest
dusky
dust
dustbin
dusted
dustier
dustiest
dusting
dustmen
dustpan
dustpans
dusts
dusty
duties
dutiful
dutifully
duty
duvet
dwarf
dwarfed
dwarfing
dwarfs
dwarves
dwell
dwelled
dweller
dwellers
dwelling
dwellings
dwells
dwelt
dwindle
dwindled
dwindles
dwindling
dye
dyed
dyeing
dyes
dying
dynamic
dynamical
dynamically
dynamics
dynamite
dynamited
dynamites
dynamiting
dynamo
dynamos
dynasties
dynasty
dysentery
dyslexia
each
eager
eagerer
eagerest
eagerly
eagerness
eagle
eagles
ear
earache
earaches
eardrum
eardrums
earl
earlier
earliest
earls
early
earmark
earmarked
earmarking
earmarks
earn
earned
earner
earners
earnest
earnestly
earnestness
earnests
earning
earnings
earns
earring
earrings
ears
earshot
earth
earthed
earthier
earthiest
earthing
earthlier
earthliest
earthly
earthquake
earthquakes
earths
earthworm
earthworms
earthy
ease
eased
easel
easels
eases
easier
easiest
easily
easing
east
easterlies
easterly
eastern
eastward
easy
easygoing
eat
eaten
eater
eating
eats
eave
eaves
eavesdrop
eavesdropped
eavesdropping
eavesdrops
ebb
ebbed
ebbing
ebbs
ebonies
ebony
eccentric
eccentricities
eccentricity
eccentrics
ecclesiastical
echo
echoed
echoes
echoing
echos
eclectic
eclipse
eclipsed
eclipses
eclipsing
ecological
ecologically
ecologist
ecologists
ecology
economic
economical
economically
economics
economies
economist
economists
economize
economized
economizes
economizing
economy
ecosystem
ecosystems
ecstasies
ecstasy
ecstatic
ecumenical
eczema
eddied
eddies
eddy
eddying
edge
edged
edger
edges
edgeways
edgewise
edgier
edgiest
edging
edgy
edible
edibles
edict
edicts
edifice
edifices
edit
edited
editing
edition
editions
editor
editorial
editorials
editors
editorship
edits
educate
educated
educates
educating
education
educational
educations
educator
educators
eel
eels
eerie
eerier
eeriest
eery
effect
effected
effecting
effective
effectively
effectiveness
effects
effectual
effeminate
effervescent
efficiency
efficient
efficiently
effigies
effigy
effort
effortless
effortlessly
efforts
effusive
effusively
egalitarian
egg
egged
egging
eggplant
eggplants
eggs
ego
egocentric
egoism
egos
egotism
egotist
egotists
eh
eigenvalue
eight
eighteen
eighteens
eighteenth
eighteenths
eighth
eighths
eighties
eightieth
eightieths
eights
eighty
either
ejaculate
ejaculated
ejaculates
ejaculating
ejaculation
ejaculations
eject
ejected
ejecting
ejection
ejections
ejects
eke
eked
ekes
eking
elaborate
elaborated
elaborately
elaborates
elaborating
elaboration
elaborations
elapse
elapsed
elapses
elapsing
elastic
elasticity
elastics
elation
elbow
elbowed
elbowing
elbows
elder
elderly
elders
eldest
elect
elected
electing
election
elections
elective
electives
elector
electoral
electorate
electorates
electors
electric
electrical
electrically
electrician
electricians
electricity
electrified
electrifies
electrify
electrifying
electrocute
electrocuted
electrocutes
electrocuting
electrocution
electrocutions
electrode
electrodes
electrolysis
electromagnetic
electron
electronic
electronically
electronics
electrons
electrostatic
elects
elegance
elegant
elegantly
elegies
elegy
element
elemental
elementary
elements
elephant
elephants
elevate
elevated
elevates
elevating
elevation
elevations
elevator
elevators
eleven
elevens
eleventh
elevenths
elf
elicit
elicited
eliciting
elicits
eligibility
eligible
eliminate
eliminated
eliminates
eliminating
elimination
eliminations
elite
elites
elitism
elitist
elk
elks
ellipse
ellipses
ellipsis
elliptic
elliptical
elm
elms
elongate
elongated
elongates
elongating
elope
eloped
elopement
elopements
elopes
eloping
eloquence
eloquent
eloquently
else
elsewhere
elucidate
elude
eluded
eludes
eluding
elusive
elves
em
email
emailed
emailing
emails
emanate
emanated
emanates
emanating
emancipate
emancipated
emancipates
emancipating
emancipation
embalm
embalmed
embalming
embalms
embankment
embankments
embargo
embargoed
embargoes
embargoing
embark
embarked
embarking
embarks
embarrass
embarrassed
embarrasses
embarrassing
embarrassment
embarrassments
embassies
embassy
embed
embedded
embedding
embeds
embellish
embellished
embellishes
embellishing
embellishment
embellishments
ember
embers
embezzle
embezzled
embezzlement
embezzles
embezzling
embitter
embittered
embittering
embitters
emblem
emblems
embodied
embodies
embodiment
embody
embodying
emboss
embossed
embosses
embossing
embrace
embraced
embraces
embracing
embroider
embroidered
embroideries
embroidering
embroiders
embroidery
embryo
embryonic
embryos
emerald
emeralds
emerge
emerged
emergence
emergencies
emergency
emergent
emerges
emerging
emigrant
emigrants
emigrate
emigrated
emigrates
emigrating
emigration
emigrations
eminence
eminences
eminent
eminently
emir
emirs
emissaries
emissary
emission
emissions
emit
emits
emitted
emitting
emotion
emotional
emotionally
emotions
emotive
empathy
emperor
emperors
emphases
emphasis
emphasize
emphasized
emphasizes
emphasizing
emphatic
emphatically
emphysema
empire
empires
empirical
employ
employe
employed
employee
employees
employer
employers
employes
employing
employment
employments
employs
emporia
emporium
emporiums
empower
empowered
empowering
empowers
empress
empresses
emptied
emptier
empties
emptiest
emptiness
empty
emptying
emulate
emulated
emulates
emulating
emulation
emulations
emulator
emulators
emulsion
emulsions
enable
enabled
enables
enabling
enact
enacted
enacting
enactment
enactments
enacts
enamel
enameled
enameling
enamelled
enamelling
enamels
encapsulate
encapsulated
encapsulates
encapsulating
encase
encased
encases
encasing
enchant
enchanted
enchanting
enchantment
enchantments
enchants
encircle
encircled
encircles
encircling
enclose
enclosed
encloses
enclosing
enclosure
enclosures
encode
encoded
encodes
encoding
encompass
encompassed
encompasses
encompassing
encore
encored
encores
encoring
encounter
encountered
encountering
encounters
encourage
encouraged
encouragement
encouragements
encourages
encouraging
encroach
encroached
encroaches
encroaching
encrypted
encryption
encumber
encumbered
encumbering
encumbers
encumbrance
encumbrances
encyclopaedia
encyclopaedias
encyclopedia
encyclopedias
end
endanger
endangered
endangering
endangers
endear
endeared
endearing
endearment
endearments
endears
endeavor
endeavored
endeavoring
endeavors
ended
endemic
endemics
ending
endings
endive
endives
endless
endlessly
endorse
endorsed
endorsement
endorsements
endorses
endorsing
endow
endowed
endowing
endowment
endowments
endows
ends
endurance
endure
endured
endures
enduring
endways
enema
enemas
enemata
enemies
enemy
energetic
energetically
energies
energy
enforce
enforced
enforcement
enforces
enforcing
engage
engaged
engagement
engagements
engages
engaging
engender
engendered
engendering
engenders
engine
engineer
engineered
engineering
engineers
engines
engrave
engraved
engraver
engravers
engraves
engraving
engravings
engross
engrossed
engrosses
engrossing
engulf
engulfed
engulfing
engulfs
enhance
enhanced
enhancement
enhancements
enhances
enhancing
enigma
enigmas
enigmatic
enjoy
enjoyable
enjoyed
enjoying
enjoyment
enjoyments
enjoys
enlarge
enlarged
enlargement
enlargements
enlarges
enlarging
enlighten
enlightened
enlightening
enlightenment
enlightens
enlist
enlisted
enlisting
enlistment
enlistments
enlists
enliven
enlivened
enlivening
enlivens
enmities
enmity
enormities
enormity
enormous
enormously
enough
enquire
enquired
enquires
enquiries
enquiring
enquiry
enrage
enraged
enrages
enraging
enrich
enriched
enriches
enriching
enrichment
enrol
enroll
enrolled
enrolling
enrollment
enrollments
enrolls
enrolment
enrolments
enrols
ensemble
ensembles
enshrine
enshrined
enshrines
enshrining
ensign
ensigns
enslave
enslaved
enslaves
enslaving
ensue
ensued
ensues
ensuing
ensure
ensured
ensures
ensuring
entail
entailed
entailing
entails
entangle
entangled
entanglement
entanglements
entangles
entangling
enter
entered
entering
enterprise
enterprises
enterprising
enters
entertain
entertained
entertainer
entertainers
entertaining
entertainment
entertainments
entertains
enthral
enthrall
enthralled
enthralling
enthralls
enthrals
enthusiasm
enthusiasms
enthusiast
enthusiastic
enthusiastically
enthusiasts
entice
enticed
enticement
enticements
entices
enticing
entire
entirely
entirety
entities
entitle
entitled
entitles
entitling
entity
entomologist
entomologists
entomology
entrails
entrance
entranced
entrances
entrancing
entrant
entrants
entrap
entrapped
entrapping
entraps
entreat
entreated
entreaties
entreating
entreats
entreaty
entrench
entrenched
entrenches
entrenching
entries
entropy
entrust
entrusted
entrusting
entrusts
entry
entwine
entwined
entwines
entwining
enumerate
enumerated
enumerates
enumerating
enumeration
enunciate
enunciated
enunciates
enunciating
enunciation
envelop
envelope
enveloped
envelopes
enveloping
envelops
enviable
envied
envies
envious
enviously
environment
environmental
environmentally
environments
environs
envisage
envisaged
envisages
envisaging
envoy
envoys
envy
envying
enzyme
enzymes
eon
eons
epaulet
epaulets
epaulette
epaulettes
ephemeral
epic
epics
epidemic
epidemics
epidermis
epidermises
epilepsy
epileptic
epileptics
epilog
epilogs
epilogue
epilogues
episode
episodes
epitaph
epitaphs
epithet
epithets
epitome
epitomes
epoch
epochs
epsilon
equal
equaled
equaling
equality
equalize
equalized
equalizes
equalizing
equalled
equalling
equally
equals
equanimity
equate
equated
equates
equating
equation
equations
equator
equatorial
equators
equestrian
equestrians
equilateral
equilaterals
equilibrium
equine
equines
equinox
equinoxes
equip
equipment
equipped
equipping
equips
equitable
equities
equity
equivalence
equivalent
equivalently
equivalents
equivocal
era
eradicate
eradicated
eradicates
eradicating
eras
erase
erased
eraser
erasers
erases
erasing
erasure
erect
erected
erecting
erection
erections
erects
ergo
ergonomic
erode
eroded
erodes
eroding
erosion
erotic
err
errand
errands
errant
erratic
erratically
erred
erring
erroneous
erroneously
error
errors
errs
erstwhile
erudite
erupt
erupted
erupting
eruption
eruptions
erupts
escalate
escalated
escalates
escalating
escalation
escalator
escalators
escapade
escapades
escape
escaped
escapes
escaping
escapism
escort
escorted
escorting
escorts
esophagi
esophagus
esophaguses
esoteric
especial
especially
espionage
essay
essayed
essaying
essays
essence
essences
essential
essentially
essentials
establish
established
establishes
establishing
establishment
establishments
estate
estates
esteem
esteemed
esteeming
esteems
esthetic
estimate
estimated
estimates
estimating
estimation
estimations
estrangement
estrangements
etch
etched
etches
etching
etchings
eternal
eternally
eternities
eternity
ether
ethereal
ethic
ethical
ethically
ethics
ethnic
ethnics
ethos
etiquette
etymological
etymologies
etymology
eulogies
eulogize
eulogized
eulogizes
eulogizing
eulogy
euphemism
euphemisms
eureka
euthanasia
evacuate
evacuated
evacuates
evacuating
evacuation
evacuations
evade
evaded
evades
evading
evaluate
evaluated
evaluates
evaluating
evaluation
evaluations
evangelical
evangelicals
evangelism
evangelist
evangelistic
evangelists
evaporate
evaporated
evaporates
evaporating
evaporation
evasion
evasions
evasive
eve
even
evened
evener
evenest
evening
evenings
evenly
evenness
evens
event
eventful
events
eventual
eventualities
eventuality
eventually
ever
evergreen
evergreens
everlasting
everlastings
evermore
every
everybody
everyday
everyone
everything
everywhere
eves
evict
evicted
evicting
eviction
evictions
evicts
evidence
evidenced
evidences
evidencing
evident
evidently
evil
eviler
evilest
eviller
evillest
evils
evocative
evoke
evoked
evokes
evoking
evolution
evolutionary
evolve
evolved
evolves
evolving
ewe
ewes
exacerbate
exacerbated
exacerbates
exacerbating
exact
exacted
exacter
exactest
exacting
exactly
exacts
exaggerate
exaggerated
exaggerates
exaggerating
exaggeration
exaggerations
exalt
exaltation
exalted
exalting
exalts
exam
examination
examinations
examine
examined
examiner
examiners
examines
examining
example
exampled
examples
exampling
exams
exasperate
exasperated
exasperates
exasperating
exasperation
excavate
excavated
excavates
excavating
excavation
excavations
exceed
exceeded
exceeding
exceedingly
exceeds
excel
excelled
excellence
excellent
excellently
excelling
excels
except
excepted
excepting
exception
exceptional
exceptionally
exceptions
excepts
excerpt
excerpted
excerpting
excerpts
excess
excesses
excessive
excessively
exchange
exchanged
exchanges
exchanging
excise
excised
excises
excising
excitable
excite
excited
excitement
excitements
excites
exciting
exclaim
exclaimed
exclaiming
exclaims
exclamation
exclamations
exclude
excluded
excludes
excluding
exclusion
exclusive
exclusively
exclusives
excommunicate
excommunicated
excommunicates
excommunicating
excommunication
excommunications
excrement
excrete
excreted
excretes
excreting
excruciating
excursion
excursions
excusable
excuse
excused
excuses
excusing
executable
execute
executed
executes
executing
execution
executioner
executioners
executions
executive
executives
executor
executors
exemplary
exemplified
exemplifies
exemplify
exemplifying
exempt
exempted
exempting
exemption
exemptions
exempts
exercise
exercised
exercises
exercising
exert
exerted
exerting
exertion
exertions
exerts
exhale
exhaled
exhales
exhaling
exhaust
exhausted
exhausting
exhaustion
exhaustive
exhausts
exhibit
exhibited
exhibiting
exhibition
exhibitions
exhibits
exhilarate
exhilarated
exhilarates
exhilarating
exhilaration
exhort
exhortation
exhortations
exhorted
exhorting
exhorts
exhume
exhumed
exhumes
exhuming
exile
exiled
exiles
exiling
exist
existed
existence
existences
existent
existential
existentially
existing
exists
exit
exited
exiting
exits
exodus
exoduses
exonerate
exonerated
exonerates
exonerating
exoneration
exorbitant
exotic
exotics
expand
expandable
expanded
expanding
expands
expanse
expanses
expansion
expansions
expansive
expatriate
expatriated
expatriates
expatriating
expect
expectancy
expectant
expectation
expectations
expected
expecting
expects
expediencies
expediency
expedient
expedients
expedite
expedited
expedites
expediting
expedition
expeditions
expel
expelled
expelling
expels
expend
expendable
expendables
expended
expending
expenditure
expenditures
expends
expense
expenses
expensive
experience
experienced
experiences
experiencing
experiment
experimental
experimentally
experimentation
experimented
experimenting
experiments
expert
expertise
expertly
experts
expiration
expire
expired
expires
expiring
expiry
explain
explained
explaining
explains
explanation
explanations
explanatory
expletive
expletives
explicable
explicit
explicitly
explode
exploded
explodes
exploding
exploit
exploitation
exploited
exploiting
exploits
exploration
explorations
explore
explored
explorer
explorers
explores
exploring
explosion
explosions
explosive
explosives
exponent
exponential
exponentially
exponents
export
exported
exporter
exporters
exporting
exports
expose
exposed
exposes
exposing
exposition
expositions
exposure
exposures
expound
expounded
expounding
expounds
express
expressed
expresses
expressing
expression
expressions
expressive
expressively
expressly
expressway
expressways
expulsion
expulsions
exquisite
extant
extemporaneous
extend
extended
extending
extends
extension
extensions
extensive
extensively
extent
extents
exterior
exteriors
exterminate
exterminated
exterminates
exterminating
extermination
exterminations
external
externally
externals
extinct
extincted
extincting
extinction
extinctions
extincts
extinguish
extinguished
extinguisher
extinguishers
extinguishes
extinguishing
extol
extoll
extolled
extolling
extolls
extols
extort
extorted
extorting
extortion
extortionate
extorts
extra
extract
extracted
extracting
extraction
extractions
extracts
extracurricular
extradite
extradited
extradites
extraditing
extradition
extraditions
extraneous
extraordinarily
extraordinary
extrapolate
extrapolated
extrapolates
extrapolating
extrapolation
extrapolations
extras
extraterrestrial
extraterrestrials
extravagance
extravagances
extravagant
extravagantly
extravert
extraverts
extreme
extremely
extremer
extremes
extremest
extremist
extremists
extremities
extremity
extricate
extricated
extricates
extricating
extrovert
extroverts
exuberance
exuberant
exude
exuded
exudes
exuding
exult
exultant
exultation
exulted
exulting
exults
eye
eyeball
eyeballed
eyeballing
eyeballs
eyebrow
eyebrows
eyed
eyeing
eyelash
eyelashes
eyelid
eyelids
eyes
eyesight
eyesore
eyesores
eyewitness
eyewitnesses
eying
fable
fables
fabric
fabricate
fabricated
fabricates
fabricating
fabrication
fabrications
fabrics
fabulous
facade
facades
face
faced
faceless
faces
facet
faceted
faceting
facetious
facets
facetted
facetting
facial
facials
facile
facilitate
facilitated
facilitates
facilitating
facilities
facility
facing
facsimile
facsimiled
facsimileing
facsimiles
fact
faction
factions
factor
factored
factorial
factories
factoring
factorization
factors
factory
facts
factual
factually
faculties
faculty
fad
fade
faded
fades
fading
fads
faeces
faggot
faggots
fagot
fagots
fail
failed
failing
failings
fails
failure
failures
faint
fainted
fainter
faintest
fainting
faintly
faints
fair
fairer
fairest
fairies
fairly
fairness
fairs
fairy
faith
faithful
faithfully
faithfulness
faithfuls
faithless
faiths
fake
faked
fakes
faking
falcon
falconry
falcons
fall
fallacies
fallacious
fallacy
fallen
fallible
falling
fallout
falls
false
falsehood
falsehoods
falsely
falser
falsest
falsetto
falsettos
falsification
falsifications
falsified
falsifies
falsify
falsifying
falsities
falsity
falter
faltered
faltering
falters
fame
famed
familiar
familiarity
familiarize
familiarized
familiarizes
familiarizing
familiars
families
family
famine
famines
famous
fan
fanatic
fanatical
fanatics
fancied
fancier
fancies
fanciest
fanciful
fancy
fancying
fanfare
fanfares
fang
fangs
fanned
fanning
fans
fantasied
fantasies
fantastic
fantastically
fantasy
fantasying
far
faraway
farce
farces
fare
fared
fares
farewell
farewells
faring
farm
farmed
farmer
farmers
farming
farmland
farms
farther
farthest
fascinate
fascinated
fascinates
fascinating
fascination
fascinations
fascism
fascist
fascists
fashion
fashionable
fashionably
fashioned
fashioning
fashions
fast
fasted
fasten
fastened
fastener
fasteners
fastening
fastenings
fastens
faster
fastest
fastidious
fasting
fasts
fat
fatal
fatalistic
fatalities
fatality
fatally
fate
fated
fateful
fates
father
fathered
fatherhood
fathering
fatherland
fatherlands
fatherly
fathers
fathom
fathomed
fathoming
fathoms
fatigue
fatigued
fatigues
fatiguing
fating
fats
fatten
fattened
fattening
fattens
fatter
fattest
fattier
fatties
fattiest
fatty
fatuous
faucet
faucets
fault
faulted
faultier
faultiest
faulting
faultless
faults
faulty
fauna
faunae
faunas
favor
favorable
favorably
favored
favoring
favorite
favorites
favoritism
favors
fawn
fawned
fawning
fawns
faze
fazed
fazes
fazing
fear
feared
fearful
fearfully
fearing
fearless
fearlessly
fears
fearsome
feasibility
feasible
feast
feasted
feasting
feasts
feat
feather
feathered
featherier
featheriest
feathering
feathers
feathery
feats
feature
featured
features
featuring
feces
fed
federal
federalism
federalist
federalists
federals
federation
federations
feds
fee
feeble
feebler
feeblest
feed
feedback
feeder
feeders
feeding
feeds
feel
feeler
feelers
feeling
feelings
feels
fees
feet
feign
feigned
feigning
feigns
feint
feinted
feinting
feints
feline
felines
fell
felled
feller
fellest
felling
fellow
fellows
fellowship
fellowships
fells
felon
felonies
felons
felony
felt
felted
felting
felts
female
females
feminine
feminines
femininity
feminism
feminist
feminists
fen
fence
fenced
fences
fencing
fend
fended
fender
fenders
fending
fends
ferment
fermentation
fermented
fermenting
ferments
fern
ferns
ferocious
ferociously
ferocity
ferret
ferreted
ferreting
ferrets
ferried
ferries
ferry
ferrying
fertile
fertility
fertilization
fertilize
fertilized
fertilizer
fertilizers
fertilizes
fertilizing
fervent
fervently
fervor
fester
festered
festering
festers
festival
festivals
festive
festivities
festivity
festoon
festooned
festooning
festoons
fetal
fetch
fetched
fetches
fetching
feted
fetich
fetiches
fetid
feting
fetish
fetishes
fetter
fettered
fettering
fetters
fetus
fetuses
feud
feudal
feudalism
feuded
feuding
feuds
fever
feverish
feverishly
fevers
few
fewer
fewest
fez
fezes
fezzes
fiasco
fiascoes
fiascos
fib
fibbed
fibber
fibbers
fibbing
fiber
fiberglass
fibers
fibs
fiche
fickle
fickler
ficklest
fiction
fictional
fictions
fictitious
fiddle
fiddled
fiddler
fiddlers
fiddles
fiddling
fiddly
fidelity
fidget
fidgeted
fidgeting
fidgets
fidgety
field
fielded
fielding
fields
fiend
fiendish
fiendishly
fiends
fierce
fiercely
fierceness
fiercer
fiercest
fierier
fieriest
fiery
fiesta
fiestas
fifteen
fifteens
fifteenth
fifteenths
fifth
fifths
fifties
fiftieth
fiftieths
fifty
fig
fight
fighter
fighters
fighting
fights
figment
figments
figs
figurative
figuratively
figure
figured
figurehead
figureheads
figures
figuring
filament
filaments
filch
filched
filches
filching
file
filed
files
filet
filets
filing
fill
filled
filler
fillet
filleted
filleting
fillets
fillies
filling
fills
filly
film
filmed
filmier
filmiest
filming
films
filmy
filter
filtered
filtering
filters
filth
filthier
filthiest
filthy
fin
final
finale
finales
finalist
finalists
finality
finalize
finalized
finalizes
finalizing
finally
finals
finance
financed
finances
financial
financially
financier
financiers
financing
finch
finches
find
finding
findings
finds
fine
fined
finely
finer
fines
finesse
finessed
finesses
finessing
finest
finger
fingered
fingering
fingernail
fingernails
fingerprint
fingerprinted
fingerprinting
fingerprints
fingers
fingertip
fingertips
finickier
finickiest
finicky
fining
finish
finished
finishes
finishing
finite
fins
fir
fire
firearm
firearms
firecracker
firecrackers
fired
firefighter
firefighters
fireflies
firefly
fireman
firemen
fireplace
fireplaces
fireproof
fireproofed
fireproofing
fireproofs
fires
fireside
firesides
firewood
firework
fireworks
firing
firm
firmed
firmer
firmest
firming
firmly
firmness
firms
firmware
firs
first
firsthand
firstly
firsts
fiscal
fiscals
fish
fished
fisher
fisheries
fisherman
fishermen
fishery
fishes
fishier
fishiest
fishing
fishy
fission
fissure
fissures
fist
fists
fit
fitful
fitness
fits
fitted
fitter
fittest
fitting
fittings
five
fiver
fives
fix
fixable
fixation
fixations
fixed
fixes
fixing
fixture
fixtures
fizz
fizzed
fizzes
fizzing
fizzle
fizzled
fizzles
fizzling
fizzy
flabbier
flabbiest
flabby
flag
flagged
flagging
flagpole
flagpoles
flagrant
flagrantly
flags
flagship
flagships
flagstone
flagstones
flail
flailed
flailing
flails
flair
flairs
flak
flake
flaked
flakes
flakier
flakiest
flaking
flaky
flamboyance
flamboyant
flamboyantly
flame
flamed
flames
flaming
flamingo
flamingoes
flamingos
flammable
flammables
flank
flanked
flanking
flanks
flannel
flanneled
flanneling
flannelled
flannelling
flannels
flap
flapjack
flapjacks
flapped
flapping
flaps
flare
flared
flares
flaring
flash
flashback
flashbacks
flashed
flasher
flashes
flashest
flashier
flashiest
flashing
flashlight
flashlights
flashy
flask
flasks
flat
flatly
flatness
flats
flatted
flatten
flattened
flattening
flattens
flatter
flattered
flatterer
flatterers
flattering
flatters
flattery
flattest
flatting
flaunt
flaunted
flaunting
flaunts
flavor
flavored
flavoring
flavorings
flavors
flaw
flawed
flawing
flawless
flawlessly
flaws
flea
fleas
fleck
flecked
flecking
flecks
fled
fledged
fledgeling
fledgelings
fledgling
fledglings
flee
fleece
fleeced
fleeces
fleecier
fleeciest
fleecing
fleecy
fleeing
flees
fleet
fleeted
fleeter
fleetest
fleeting
fleets
flesh
fleshed
fleshes
fleshier
fleshiest
fleshing
fleshy
flew
flex
flexed
flexes
flexibility
flexible
flexibly
flexing
flick
flicked
flicker
flickered
flickering
flickers
flicking
flicks
flied
flier
fliers
flies
fliest
flight
flightier
flightiest
flightless
flights
flighty
flimsier
flimsiest
flimsiness
flimsy
flinch
flinched
flinches
flinching
fling
flinging
flings
flint
flints
flip
flippant
flipped
flipper
flippers
flippest
flipping
flips
flirt
flirtation
flirtations
flirtatious
flirted
flirting
flirts
flit
flits
flitted
flitting
float
floated
floating
floats
flock
flocked
flocking
flocks
flog
flogged
flogging
flogs
flood
flooded
flooder
flooding
floodlight
floodlighted
floodlighting
floodlights
floods
floor
floored
flooring
floors
flop
flopped
floppier
floppies
floppiest
flopping
floppy
flops
flora
florae
floral
floras
florid
florist
florists
floss
flossed
flosses
flossing
flotilla
flotillas
flounce
flounced
flounces
flouncing
flounder
floundered
floundering
flounders
flour
floured
flouring
flourish
flourished
flourishes
flourishing
flours
flout
flouted
flouting
flouts
flow
flowed
flower
flowered
flowerier
floweriest
flowering
flowers
flowery
flowing
flown
flows
flu
fluctuate
fluctuated
fluctuates
fluctuating
fluctuation
fluctuations
flue
fluency
fluent
fluently
flues
fluff
fluffed
fluffier
fluffiest
fluffing
fluffs
fluffy
fluid
fluids
fluke
flukes
flung
flunk
flunked
flunkey
flunkeys
flunkie
flunkies
flunking
flunks
flunky
fluorescent
flurried
flurries
flurry
flurrying
flush
flushed
flusher
flushes
flushest
flushing
fluster
flustered
flustering
flusters
flute
fluted
flutes
fluting
flutist
flutists
flutter
fluttered
fluttering
flutters
flux
fluxed
fluxes
fluxing
fly
flyer
flyers
flying
flyover
flyovers
foal
foaled
foaling
foals
foam
foamed
foamier
foamiest
foaming
foams
foamy
focal
foci
focus
focused
focuses
focusing
focussed
focusses
focussing
fodder
fodders
foe
foes
foetal
foetus
foetuses
fog
fogey
fogeys
fogged
foggier
foggiest
fogging
foggy
foghorn
foghorns
fogies
fogs
fogy
foible
foibles
foil
foiled
foiling
foils
foist
foisted
foisting
foists
fold
folded
folder
folders
folding
folds
foliage
folk
folklore
folks
folksier
folksiest
folksy
follies
follow
followed
follower
followers
following
followings
follows
folly
foment
fomented
fomenting
foments
fond
fonder
fondest
fondle
fondled
fondles
fondling
fondly
fondness
font
fonts
food
foods
foodstuff
foodstuffs
fool
fooled
foolhardier
foolhardiest
foolhardy
fooling
foolish
foolishly
foolishness
foolproof
fools
foot
footage
football
footballs
footed
foothill
foothills
foothold
footholds
footing
footings
footlights
footnote
footnoted
footnotes
footnoting
footpath
footpaths
footprint
footprints
foots
footstep
footsteps
footstool
footstools
footwear
footwork
for
fora
forage
foraged
forages
foraging
foray
forayed
foraying
forays
forbad
forbade
forbear
forbearance
forbearing
forbears
forbid
forbidden
forbidding
forbiddings
forbids
forbore
forborne
force
forced
forceful
forcefully
forceps
forces
forcible
forcibly
forcing
ford
forded
fording
fords
fore
forearm
forearmed
forearming
forearms
forebode
foreboded
forebodes
foreboding
forebodings
forecast
forecasted
forecasting
forecasts
forefather
forefathers
forefinger
forefingers
forefront
forefronts
forego
foregoes
foregoing
foregone
foreground
foregrounded
foregrounding
foregrounds
forehead
foreheads
foreign
foreigner
foreigners
foreleg
forelegs
foreman
foremen
foremost
forensic
forensics
foreplay
forerunner
forerunners
fores
foresaw
foresee
foreseeable
foreseeing
foreseen
foresees
foreshadow
foreshadowed
foreshadowing
foreshadows
foresight
foreskin
foreskins
forest
forestall
forestalled
forestalling
forestalls
forested
foresting
forestry
forests
foreswear
foreswearing
foreswears
foreswore
foresworn
foretaste
foretasted
foretastes
foretasting
foretell
foretelling
foretells
forethought
foretold
forever
forewarn
forewarned
forewarning
forewarns
forewent
foreword
forewords
forfeit
forfeited
forfeiting
forfeits
forgave
forge
forged
forger
forgeries
forgers
forgery
forges
forget
forgetful
forgetfulness
forgets
forgetting
forging
forgive
forgiven
forgiveness
forgives
forgiving
forgo
forgoes
forgoing
forgone
forgot
forgotten
fork
forked
forking
forks
forlorn
form
formal
formalities
formality
formalize
formalized
formalizes
formalizing
formally
formals
format
formation
formations
formative
formats
formatted
formatting
formed
former
formerly
formidable
forming
formless
forms
formula
formulae
formulas
formulate
formulated
formulates
formulating
formulation
formulations
fornication
forsake
forsaken
forsakes
forsaking
forsook
forswear
forswearing
forswears
forswore
forsworn
fort
forte
fortes
forth
forthcoming
forthright
forthwith
forties
fortieth
fortieths
fortification
fortifications
fortified
fortifies
fortify
fortifying
fortitude
fortnight
fortnightly
fortress
fortresses
forts
fortuitous
fortunate
fortunately
fortune
fortunes
forty
forum
forums
forward
forwarded
forwarder
forwardest
forwarding
forwards
forwent
fossil
fossilize
fossilized
fossilizes
fossilizing
fossils
foster
fostered
fostering
fosters
fought
foul
fouled
fouler
foulest
fouling
fouls
found
foundation
foundations
founded
founder
foundered
foundering
founders
founding
foundling
foundlings
foundries
foundry
founds
fount
fountain
fountains
founts
four
fours
fourteen
fourteens
fourteenth
fourteenths
fourth
fourths
fowl
fowled
fowling
fowls
fox
foxed
foxes
foxier
foxiest
foxing
foxy
foyer
foyers
fracas
fracases
fractal
fraction
fractional
fractions
fracture
fractured
fractures
fracturing
fragile
fragility
fragment
fragmentary
fragmentation
fragmented
fragmenting
fragments
fragrance
fragrances
fragrant
frail
frailer
frailest
frailties
frailty
frame
framed
frames
framework
frameworks
framing
franc
franchise
franchised
franchises
franchising
francs
frank
franked
franker
frankest
frankfurter
frankfurters
franking
frankly
franks
frantic
frantically
fraternal
fraternities
fraternity
fraternize
fraternized
fraternizes
fraternizing
fraud
frauds
fraudulent
fraudulently
fraught
fray
frayed
fraying
frays
freak
freaked
freaking
freaks
freckle
freckled
freckles
freckling
free
freed
freedom
freedoms
freehand
freeing
freelance
freely
freer
frees
freest
freeway
freeways
freeze
freezer
freezers
freezes
freezing
freight
freighted
freighter
freighters
freighting
freights
french
frenzied
frenzies
frenzy
frequencies
frequency
frequent
frequented
frequenter
frequentest
frequenting
frequently
frequents
fresh
freshen
freshened
freshening
freshens
fresher
freshest
freshly
freshman
freshmen
freshness
freshwater
fret
fretful
fretfully
frets
fretted
fretting
friar
friars
friction
fried
friend
friendlier
friendlies
friendliest
friendliness
friendly
friends
friendship
friendships
fries
frieze
friezes
frigate
frigates
fright
frighted
frighten
frightened
frightening
frighteningly
frightens
frightful
frightfully
frighting
frights
frigid
frigidity
frill
frillier
frilliest
frills
frilly
fringe
fringed
fringes
fringing
frisk
frisked
friskier
friskiest
frisking
frisks
frisky
fritter
frittered
frittering
fritters
frivolities
frivolity
frivolous
frizzier
frizziest
frizzy
fro
frock
frocks
frog
frogs
frolic
frolicked
frolicking
frolics
from
frond
fronds
front
frontage
frontages
frontal
fronted
frontier
frontiers
fronting
fronts
frost
frostbit
frostbite
frostbites
frostbiting
frostbitten
frosted
frostier
frostiest
frosting
frosts
frosty
froth
frothed
frothier
frothiest
frothing
froths
frothy
frown
frowned
frowning
frowns
froze
frozen
frugal
frugality
frugally
fruit
fruited
fruitful
fruitier
fruitiest
fruiting
fruition
fruitless
fruitlessly
fruits
fruity
frustrate
frustrated
frustrates
frustrating
frustration
frustrations
fry
frying
fudge
fudged
fudges
fudging
fuel
fueled
fueling
fuelled
fuelling
fuels
fugitive
fugitives
fulcra
fulcrum
fulcrums
fulfil
fulfill
fulfilled
fulfilling
fulfillment
fulfills
fulfilment
fulfils
full
fulled
fuller
fullest
fulling
fullness
fulls
fully
fulness
fumble
fumbled
fumbles
fumbling
fume
fumed
fumes
fumigate
fumigated
fumigates
fumigating
fumigation
fuming
fun
function
functional
functionality
functionally
functioned
functioning
functions
fund
fundamental
fundamentalism
fundamentalist
fundamentalists
fundamentally
fundamentals
funded
funding
funds
funeral
funerals
fungi
fungicide
fungicides
fungus
funguses
funnel
funneled
funneling
funnelled
funnelling
funnels
funner
funnest
funnier
funnies
funniest
funnily
funny
fur
furies
furious
furiously
furl
furled
furling
furlong
furlongs
furlough
furloughed
furloughing
furloughs
furls
furnace
furnaces
furnish
furnished
furnishes
furnishing
furnishings
furniture
furor
furors
furred
furrier
furriest
furring
furrow
furrowed
furrowing
furrows
furry
furs
further
furthered
furthering
furthermore
furthers
furthest
furtive
furtively
furtiveness
fury
fuse
fused
fuselage
fuselages
fuses
fusing
fusion
fuss
fussed
fusses
fussier
fussiest
fussing
fussy
futile
futility
future
futures
futuristic
fuze
fuzed
fuzes
fuzing
fuzz
fuzzed
fuzzes
fuzzier
fuzziest
fuzzing
fuzzy
gab
gabbed
gabbing
gable
gables
gabs
gadget
gadgets
gag
gage
gaged
gages
gagged
gagging
gaging
gags
gaiety
gaily
gain
gained
gainful
gaining
gains
gait
gaits
gal
gala
galactic
galas
galaxies
galaxy
gale
gales
gall
gallant
gallantry
gallants
galled
galleries
gallery
galley
galleys
galling
gallivant
gallivanted
gallivanting
gallivants
gallon
gallons
gallop
galloped
galloping
gallops
gallows
gallowses
galls
galore
gals
galvanize
galvanized
galvanizes
galvanizing
gambit
gambits
gamble
gambled
gambler
gamblers
gambles
gambling
game
gamed
gamer
games
gamest
gaming
gamma
gamut
gamuts
gander
ganders
gang
ganged
ganging
gangling
gangplank
gangplanks
gangrene
gangrened
gangrenes
gangrening
gangs
gangster
gangsters
gangway
gangways
gap
gape
gaped
gapes
gaping
gaps
garage
garaged
garages
garaging
garb
garbage
garbed
garbing
garble
garbled
garbles
garbling
garbs
garden
gardened
gardener
gardeners
gardenia
gardenias
gardening
gardens
gargle
gargled
gargles
gargling
gargoyle
gargoyles
garish
garland
garlanded
garlanding
garlands
garlic
garment
garments
garnet
garnets
garnish
garnished
garnishes
garnishing
garret
garrets
garrison
garrisoned
garrisoning
garrisons
garrulous
garter
garters
gas
gaseous
gases
gash
gashed
gashes
gashing
gasket
gaskets
gasolene
gasoline
gasp
gasped
gasping
gasps
gassed
gasses
gassing
gastric
gate
gated
gates
gateway
gateways
gather
gathered
gathering
gatherings
gathers
gating
gaudier
gaudiest
gaudy
gauge
gauged
gauges
gauging
gaunt
gaunter
gauntest
gauntlet
gauntlets
gauze
gave
gavel
gavels
gawk
gawked
gawkier
gawkiest
gawking
gawks
gawky
gay
gayer
gayest
gayety
gayly
gays
gaze
gazed
gazelle
gazelles
gazes
gazette
gazetted
gazettes
gazetting
gazing
gear
geared
gearing
gears
gee
geed
geeing
gees
geese
gel
gelatin
gelatine
geld
gelded
gelding
geldings
gelds
gelt
gem
gems
gender
genders
gene
genealogical
genealogies
genealogy
genera
general
generality
generalization
generalizations
generalize
generalized
generalizes
generalizing
generally
generals
generate
generated
generates
generating
generation
generations
generator
generators
generic
generics
generosities
generosity
generous
generously
genes
geneses
genesis
genetic
genetically
geneticist
geneticists
genetics
genial
genially
genie
genies
genii
genital
genitals
genius
geniuses
genocide
genre
genres
gent
gentile
gentiles
gentility
gentle
gentled
gentleman
gentlemen
gentleness
gentler
gentles
gentlest
gentling
gently
gentries
gentry
gents
genuine
genuinely
genuineness
genus
genuses
geographic
geographical
geographically
geographies
geography
geological
geologies
geologist
geologists
geology
geometric
geometries
geometry
geranium
geraniums
gerbil
gerbils
germ
germicide
germicides
germinate
germinated
germinates
germinating
germination
germs
gestation
gesticulate
gesticulated
gesticulates
gesticulating
gesture
gestured
gestures
gesturing
get
getaway
getaways
gets
getting
geyser
geysers
ghastlier
ghastliest
ghastly
ghetto
ghettoes
ghettos
ghost
ghosted
ghosting
ghostlier
ghostliest
ghostly
ghosts
ghoul
ghouls
giant
giants
gibber
gibbered
gibbering
gibberish
gibbers
gibe
gibed
gibes
gibing
giddier
giddiest
giddiness
giddy
gift
gifted
gifting
gifts
gig
gigantic
gigged
gigging
giggle
giggled
giggles
giggling
gigs
gild
gilded
gilding
gilds
gill
gills
gilt
gilts
gimme
gimmick
gimmicks
gin
ginger
gingerbread
gingerly
gingham
ginned
ginning
gins
giraffe
giraffes
girder
girders
girdle
girdled
girdles
girdling
girl
girlfriend
girlfriends
girlhood
girlhoods
girlish
girls
girth
girths
gist
give
given
givens
gives
giving
gizzard
gizzards
glacial
glacier
glaciers
glad
gladden
gladdened
gladdening
gladdens
gladder
gladdest
glade
glades
gladiator
gladiators
gladly
glads
glamor
glamored
glamoring
glamorize
glamorized
glamorizes
glamorizing
glamorous
glamors
glamour
glamoured
glamouring
glamourize
glamourized
glamourizes
glamourizing
glamourous
glamours
glance
glanced
glances
glancing
gland
glands
glandular
glare
glared
glares
glaring
glass
glassed
glasses
glassier
glassiest
glassing
glassware
glassy
glaze
glazed
glazes
glazing
gleam
gleamed
gleaming
gleams
glean
gleaned
gleaning
gleans
glee
glen
glens
glib
glibber
glibbest
glibly
glide
glided
glider
gliders
glides
gliding
glimmer
glimmered
glimmering
glimmers
glimpse
glimpsed
glimpses
glimpsing
glint
glinted
glinting
glints
glisten
glistened
glistening
glistens
glitter
glittered
glittering
glitters
gloat
gloated
gloating
gloats
global
globally
globe
globes
globular
globule
globules
gloom
gloomier
gloomiest
gloomy
gloried
glories
glorification
glorified
glorifies
glorify
glorifying
glorious
gloriously
glory
glorying
gloss
glossaries
glossary
glossed
glosses
glossier
glossies
glossiest
glossing
glossy
glove
gloved
gloves
gloving
glow
glowed
glower
glowered
glowering
glowers
glowing
glows
glucose
glue
glued
glueing
glues
gluing
glum
glummer
glummest
glut
gluts
glutted
glutting
glutton
gluttons
gluttony
glycerin
glycerine
gnarl
gnarled
gnarling
gnarls
gnash
gnashed
gnashes
gnashing
gnat
gnats
gnaw
gnawed
gnawing
gnawn
gnaws
gnome
gnomes
gnu
gnus
go
goad
goaded
goading
goads
goal
goalie
goalies
goalkeeper
goalkeepers
goals
goat
goatee
goatees
goats
gob
gobbed
gobbing
gobble
gobbled
gobbles
gobbling
goblet
goblets
goblin
goblins
gobs
god
godchild
godchildren
goddess
goddesses
godfather
godfathers
godless
godlier
godliest
godlike
godly
godmother
godmothers
godparent
godparents
gods
godsend
godsends
goes
goggle
goggles
going
gold
golden
goldener
goldenest
goldfish
goldfishes
golds
goldsmith
goldsmiths
golf
golfed
golfer
golfers
golfing
golfs
gondola
gondolas
gone
goner
goners
gong
gonged
gonging
gongs
gonna
goo
good
goodby
goodbye
goodie
goodies
goodness
goodnight
goods
goodwill
goody
gooey
goof
goofed
goofier
goofiest
goofing
goofs
goofy
gooier
gooiest
goon
goons
goose
goosed
gooses
goosing
gopher
gophers
gore
gored
gores
gorge
gorged
gorgeous
gorges
gorging
gorier
goriest
gorilla
gorillas
goring
gory
gosh
gosling
goslings
gospel
gospels
gossamer
gossip
gossiped
gossiping
gossipped
gossipping
gossips
got
gotten
gouge
gouged
gouges
gouging
goulash
goulashes
gourd
gourds
gourmet
gourmets
gout
govern
governed
governess
governesses
governing
government
governmental
governments
governor
governors
governs
gown
gowned
gowning
gowns
grab
grabbed
grabber
grabbing
grabs
grace
graced
graceful
gracefully
graceless
graces
gracing
gracious
graciously
graciousness
gradation
gradations
grade
graded
grader
grades
gradient
gradients
grading
gradual
gradually
graduate
graduated
graduates
graduating
graduation
graduations
graffiti
graffito
graft
grafted
grafting
grafts
grain
grains
gram
grammar
grammars
grammatical
grammatically
gramophone
grams
grand
grandchild
grandchildren
granddaughter
granddaughters
grander
grandest
grandeur
grandfather
grandfathered
grandfathering
grandfathers
grandiose
grandly
grandmother
grandmothers
grandparent
grandparents
grands
grandson
grandsons
grandstand
grandstanded
grandstanding
grandstands
granite
grannie
grannies
granny
granola
grant
granted
granting
grants
granular
granule
granules
grape
grapefruit
grapefruits
grapes
grapevine
grapevines
graph
graphed
graphic
graphical
graphically
graphics
graphing
graphite
graphs
grapple
grappled
grapples
grappling
grasp
grasped
grasping
grasps
grass
grassed
grasses
grasshopper
grasshoppers
grassier
grassiest
grassing
grassy
grate
grated
grateful
gratefully
grater
graters
grates
gratification
gratifications
gratified
gratifies
gratify
gratifying
grating
gratings
gratitude
gratuities
gratuitous
gratuitously
gratuity
grave
graved
gravel
graveled
graveling
gravelled
gravelling
gravels
gravely
graven
graver
graves
gravest
gravestone
gravestones
graveyard
graveyards
gravies
graving
gravitate
gravitated
gravitates
gravitating
gravitation
gravitational
gravity
gravy
gray
grayed
grayer
grayest
graying
grays
graze
grazed
grazes
grazing
grease
greased
greases
greasier
greasiest
greasing
greasy
great
greater
greatest
greatly
greatness
greats
greed
greedier
greediest
greedily
greediness
greedy
green
greenback
greenbacks
greened
greener
greenery
greenest
greenhorn
greenhorns
greenhouse
greenhouses
greening
greens
greet
greeted
greeting
greetings
greets
gregarious
gremlin
gremlins
grenade
grenades
grew
grey
greyed
greyer
greyest
greyhound
greyhounds
greying
greys
grid
griddle
griddles
gridiron
gridirons
grids
grief
griefs
grievance
grievances
grieve
grieved
grieves
grieving
grievous
grill
grille
grilled
grilles
grilling
grills
grim
grimace
grimaced
grimaces
grimacing
grime
grimed
grimes
grimier
grimiest
griming
grimly
grimmer
grimmest
grimy
grin
grind
grinder
grinders
grinding
grinds
grindstone
grindstones
grinned
grinning
grins
grip
gripe
griped
gripes
griping
gripped
gripping
grips
grislier
grisliest
grisly
gristle
grit
grits
gritted
grittier
grittiest
gritting
gritty
grizzled
grizzlier
grizzlies
grizzliest
grizzly
groan
groaned
groaning
groans
grocer
groceries
grocers
grocery
groggier
groggiest
groggy
groin
groins
groom
groomed
grooming
grooms
groove
grooved
grooves
groovier
grooviest
grooving
groovy
grope
groped
gropes
groping
gross
grossed
grosser
grosses
grossest
grossing
grossly
grotesque
grotesques
grotto
grottoes
grottos
grouch
grouched
grouches
grouchier
grouchiest
grouching
grouchy
ground
grounded
grounding
groundless
grounds
groundwork
group
grouped
grouper
groupers
grouping
groupings
groups
grouse
groused
grouses
grousing
grove
grovel
groveled
groveling
grovelled
grovelling
grovels
groves
grow
grower
growers
growing
growl
growled
growling
growls
grown
grows
growth
growths
grub
grubbed
grubbier
grubbiest
grubbing
grubby
grubs
grudge
grudged
grudges
grudging
gruel
grueling
gruelling
gruellings
gruesome
gruesomer
gruesomest
gruff
gruffer
gruffest
gruffly
grumble
grumbled
grumbles
grumbling
grumpier
grumpiest
grumpy
grunt
grunted
grunting
grunts
guarantee
guaranteed
guaranteeing
guarantees
guarantor
guarantors
guard
guarded
guardian
guardians
guarding
guards
gubernatorial
guerilla
guerillas
guerrilla
guerrillas
guess
guessable
guessed
guesses
guessing
guesswork
guest
guested
guesting
guests
guffaw
guffawed
guffawing
guffaws
guidance
guide
guidebook
guidebooks
guided
guideline
guidelines
guides
guiding
guild
guilds
guile
guillotine
guillotined
guillotines
guillotining
guilt
guiltier
guiltiest
guiltily
guiltless
guilty
guinea
guise
guises
guitar
guitarist
guitars
gulch
gulches
gulf
gulfs
gull
gulled
gullet
gullets
gulley
gullible
gullies
gulling
gulls
gully
gulp
gulped
gulping
gulps
gum
gumdrop
gumdrops
gummed
gummier
gummiest
gumming
gummy
gumption
gums
gun
gunfire
gunman
gunmen
gunned
gunner
gunners
gunning
gunpowder
guns
gunshot
gunshots
guppies
guppy
gurgle
gurgled
gurgles
gurgling
guru
gurus
gush
gushed
gusher
gushers
gushes
gushing
gust
gusted
gustier
gustiest
gusting
gusts
gusty
gut
guts
gutted
gutter
guttered
guttering
gutters
gutting
guy
guyed
guying
guys
guzzle
guzzled
guzzles
guzzling
gybe
gybed
gybes
gybing
gym
gymnasia
gymnasium
gymnasiums
gymnast
gymnastics
gymnasts
gyms
gynecologist
gynecologists
gynecology
gyrate
gyrated
gyrates
gyrating
gyration
gyrations
gyroscope
gyroscopes
ha
habit
habitable
habitat
habitation
habitations
habitats
habits
habitual
habitually
hack
hacked
hacker
hackers
hacking
hackney
hackneyed
hackneying
hackneys
hacks
hacksaw
hacksaws
had
haddock
haddocks
haemoglobin
haemophilia
haemorrhage
haemorrhaged
haemorrhages
haemorrhaging
hag
haggard
haggle
haggled
haggles
haggling
hags
hah
hail
hailed
hailing
hails
hailstone
hailstones
hair
haircut
haircuts
hairdo
hairdos
hairdresser
hairdressers
haired
hairier
hairiest
hairline
hairlines
hairs
hairy
hale
haled
haler
hales
halest
half
halfway
halibut
halibuts
haling
hall
hallelujah
hallelujahs
hallmark
hallmarked
hallmarking
hallmarks
halls
hallucination
hallucinations
hallway
hallways
halo
haloed
haloes
haloing
halon
halos
halt
halted
halter
haltered
haltering
halters
halting
halts
halve
halved
halves
halving
ham
hamburger
hamburgers
hamlet
hamlets
hammed
hammer
hammered
hammering
hammers
hamming
hammock
hammocks
hamper
hampered
hampering
hampers
hams
hamster
hamsters
hamstring
hamstringing
hamstrings
hamstrung
hand
handbag
handbags
handbook
handbooks
handcuff
handcuffed
handcuffing
handcuffs
handed
handedness
handful
handfuls
handicap
handicapped
handicapping
handicaps
handicraft
handicrafts
handier
handiest
handing
handiwork
handkerchief
handkerchiefs
handkerchieves
handle
handlebar
handlebars
handled
handler
handlers
handles
handling
handmade
handout
handouts
handrail
handrails
hands
handsful
handshake
handshakes
handsome
handsomer
handsomest
handwriting
handy
hang
hangar
hangars
hanged
hanger
hangers
hanging
hangings
hangout
hangouts
hangover
hangovers
hangs
hanker
hankered
hankering
hankers
haphazard
hapless
happen
happened
happening
happenings
happens
happier
happiest
happily
happiness
happy
harangue
harangued
harangues
haranguing
harass
harassed
harasses
harassing
harassment
harbor
harbored
harboring
harbors
hard
hardback
harden
hardened
hardening
hardens
harder
hardest
hardier
hardiest
hardline
hardliner
hardliners
hardly
hardship
hardships
hardware
hardwood
hardwoods
hardy
hare
harebrained
hared
harem
harems
hares
haring
hark
harked
harking
harks
harlot
harlots
harm
harmed
harmful
harmfully
harming
harmless
harmlessly
harmonic
harmonica
harmonicas
harmonies
harmonious
harmonize
harmonized
harmonizes
harmonizing
harmony
harms
harness
harnessed
harnesses
harnessing
harp
harped
harping
harpist
harpists
harpoon
harpooned
harpooning
harpoons
harps
harpsichord
harpsichords
harried
harries
harrow
harrowed
harrowing
harrows
harry
harrying
harsh
harsher
harshest
harshly
harshness
hart
harts
harvest
harvested
harvester
harvesters
harvesting
harvests
has
hash
hashed
hashes
hashing
hassle
hassled
hassles
hassling
haste
hasted
hasten
hastened
hastening
hastens
hastes
hastier
hastiest
hastily
hasting
hasty
hat
hatch
hatched
hatches
hatchet
hatchets
hatching
hate
hated
hateful
hatefully
hates
hating
hatred
hatreds
hats
hatted
hatting
haughtier
haughtiest
haughtily
haughtiness
haughty
haul
hauled
hauling
hauls
haunt
haunted
haunting
haunts
have
haven
havens
haves
having
havoc
hawk
hawked
hawking
hawks
hay
hayed
haying
hays
haystack
haystacks
haywire
hazard
hazarded
hazarding
hazardous
hazards
haze
hazed
hazel
hazels
hazes
hazier
haziest
hazing
hazy
he
head
headache
headaches
headed
header
headers
headfirst
headier
headiest
heading
headings
headland
headlands
headlight
headlights
headline
headlined
headlines
headlining
headlong
headmaster
headphone
headphones
headquarter
headquarters
headrest
headrests
headroom
heads
headstone
headstones
headstrong
headway
heady
heal
healed
healer
healers
healing
heals
health
healthful
healthier
healthiest
healthy
heap
heaped
heaping
heaps
hear
heard
hearing
hearings
hears
hearsay
hearse
hearses
heart
heartache
heartaches
heartbeat
heartbeats
heartbreak
heartbreaks
heartbroken
heartburn
hearten
heartened
heartening
heartens
heartfelt
hearth
hearths
heartier
hearties
heartiest
heartily
heartless
hearts
hearty
heat
heated
heatedly
heater
heaters
heath
heathen
heathens
heather
heating
heats
heave
heaved
heaven
heavenlier
heavenliest
heavenly
heavens
heaves
heavier
heavies
heaviest
heavily
heaviness
heaving
heavy
heavyweight
heavyweights
heckle
heckled
heckler
hecklers
heckles
heckling
hectic
hedge
hedged
hedgehog
hedgehogs
hedges
hedging
heed
heeded
heeding
heedless
heeds
heel
heeled
heeling
heels
heftier
heftiest
hefty
heifer
heifers
height
heighten
heightened
heightening
heightens
heights
heinous
heir
heirloom
heirlooms
heirs
held
helicopter
helicoptered
helicoptering
helicopters
heliport
heliports
helium
hell
hellish
hello
hellos
helm
helmet
helmets
helms
help
helped
helper
helpers
helpful
helpfully
helping
helpings
helpless
helplessly
helps
hem
hemisphere
hemispheres
hemlock
hemlocks
hemmed
hemming
hemoglobin
hemophilia
hemorrhage
hemorrhaged
hemorrhages
hemorrhaging
hemp
hems
hen
hence
henceforth
henchman
henchmen
hens
hepatitis
her
herald
heralded
heralding
heralds
herb
herbivorous
herbs
herd
herded
herding
herds
here
hereabouts
hereafter
hereafters
hereby
hereditary
heredity
herein
heresies
heresy
heretic
heretical
heretics
herewith
heritage
heritages
hermaphrodite
hermit
hermits
hernia
herniae
hernias
hero
heroes
heroic
heroin
heroine
heroins
heroism
heron
herons
heros
herpes
herring
herrings
hers
herself
hes
hesitancy
hesitant
hesitate
hesitated
hesitates
hesitating
hesitation
hesitations
heterogeneous
heterosexual
heterosexuality
heterosexuals
heuristic
hew
hewed
hewing
hewn
hews
hexadecimal
hexagon
hexagonal
hexagons
hey
heyday
heydays
hi
hiatus
hiatuses
hibernate
hibernated
hibernates
hibernating
hibernation
hiccup
hiccuped
hiccuping
hiccups
hick
hickories
hickory
hicks
hid
hidden
hide
hideaway
hideaways
hided
hideous
hideously
hides
hiding
hierarchical
hierarchies
hierarchy
hieroglyphic
hieroglyphics
high
highbrow
highbrows
higher
highest
highjack
highjacked
highjacking
highjacks
highland
highlands
highlight
highlighted
highlighting
highlights
highly
highs
highway
highways
hijack
hijacked
hijacking
hijacks
hike
hiked
hiker
hikers
hikes
hiking
hilarious
hilarity
hill
hillbillies
hillbilly
hillier
hilliest
hills
hillside
hillsides
hilly
hilt
hilts
him
hims
himself
hind
hinder
hindered
hindering
hinders
hindrance
hindrances
hinds
hindsight
hinge
hinged
hinges
hinging
hint
hinted
hinterland
hinterlands
hinting
hints
hip
hipped
hipper
hippest
hippie
hippies
hipping
hippopotami
hippopotamus
hippopotamuses
hippy
hips
hire
hired
hires
hiring
his
hiss
hissed
hisses
hissing
histogram
historian
historians
historic
historical
historically
histories
history
hit
hitch
hitched
hitches
hitchhike
hitchhiked
hitchhiker
hitchhikers
hitchhikes
hitchhiking
hitching
hither
hitherto
hits
hitting
hive
hived
hives
hiving
ho
hoard
hoarded
hoarder
hoarders
hoarding
hoards
hoarse
hoarseness
hoarser
hoarsest
hoax
hoaxed
hoaxes
hoaxing
hobbies
hobbit
hobble
hobbled
hobbles
hobbling
hobby
hobbyhorse
hobbyhorses
hobgoblin
hobgoblins
hobnob
hobnobbed
hobnobbing
hobnobs
hobo
hoboes
hobos
hock
hocked
hockey
hocking
hocks
hodgepodge
hodgepodges
hoe
hoed
hoeing
hoes
hog
hogged
hogging
hogs
hoist
hoisted
hoisting
hoists
hold
holder
holders
holding
holds
holdup
holdups
hole
holed
holes
holiday
holidayed
holidaying
holidays
holier
holiest
holiness
holing
holler
hollered
hollering
hollers
hollies
hollow
hollowed
hollower
hollowest
hollowing
hollows
holly
holocaust
holocausts
holster
holstered
holstering
holsters
holy
homage
homages
home
homed
homeland
homelands
homeless
homelier
homeliest
homely
homemade
homes
homesick
homesickness
homespun
homestead
homesteaded
homesteading
homesteads
homeward
homework
homey
homeys
homicidal
homicide
homicides
homie
homier
homies
homiest
homing
homogeneous
homogenize
homogenized
homogenizes
homogenizing
homonym
homonyms
homophobic
homosexual
homosexuality
homosexuals
homy
hone
honed
hones
honest
honester
honestest
honestly
honesty
honey
honeycomb
honeycombed
honeycombing
honeycombs
honeyed
honeying
honeymoon
honeymooned
honeymooning
honeymoons
honeys
honeysuckle
honeysuckles
honied
honing
honk
honked
honking
honks
honor
honorable
honorary
honored
honoring
honors
hood
hooded
hooding
hoodlum
hoodlums
hoods
hoodwink
hoodwinked
hoodwinking
hoodwinks
hoof
hoofed
hoofing
hoofs
hook
hooked
hooking
hooks
hoop
hooped
hooping
hoops
hoorah
hoorahs
hooray
hoorayed
hooraying
hoorays
hoot
hooted
hooter
hooting
hoots
hooves
hop
hope
hoped
hopeful
hopefully
hopefuls
hopeless
hopelessly
hopes
hoping
hopped
hopper
hopping
hops
hopscotch
hopscotched
hopscotches
hopscotching
horde
horded
hordes
hording
horizon
horizons
horizontal
horizontally
horizontals
hormone
hormones
horn
horned
hornet
hornets
hornier
horniest
horns
horny
horoscope
horoscopes
horrendous
horrendously
horrible
horribly
horrid
horrific
horrified
horrifies
horrify
horrifying
horror
horrors
horse
horseback
horsed
horseman
horseplay
horsepower
horseradish
horseradishes
horses
horseshoe
horseshoed
horseshoeing
horseshoes
horsing
horticultural
horticulture
hose
hosed
hoses
hosiery
hosing
hospitable
hospital
hospitality
hospitalization
hospitalizations
hospitalize
hospitalized
hospitalizes
hospitalizing
hospitals
host
hostage
hostages
hosted
hostel
hosteled
hosteling
hostelled
hostelling
hostels
hostess
hostessed
hostesses
hostessing
hostile
hostiles
hostility
hosting
hosts
hot
hotbed
hotbeds
hotel
hotels
hothead
hotheaded
hotheads
hotly
hotter
hottest
hound
hounded
hounding
hounds
hour
hourglass
hourglasses
hourly
hours
house
houseboat
houseboats
housed
household
households
housekeeper
housekeepers
houses
housewarming
housewarmings
housewife
housewives
housework
housing
housings
hove
hovel
hovels
hover
hovered
hovering
hovers
how
however
howl
howled
howling
howls
hows
hub
hubbub
hubbubs
hubs
huddle
huddled
huddles
huddling
hue
hued
hues
huff
huffed
huffier
huffiest
huffing
huffs
huffy
hug
huge
hugely
huger
hugest
hugged
hugging
hugs
huh
hulk
hulking
hulks
hull
hullabaloo
hullabaloos
hulled
hulling
hulls
hum
human
humane
humanely
humaner
humanest
humanism
humanist
humanitarian
humanitarians
humanities
humanity
humanize
humanized
humanizes
humanizing
humanly
humans
humble
humbled
humbler
humbles
humblest
humbling
humbly
humbug
humdrum
humid
humidified
humidifies
humidify
humidifying
humidity
humiliate
humiliated
humiliates
humiliating
humiliation
humiliations
humility
hummed
humming
hummingbird
hummingbirds
humor
humored
humoring
humorist
humorists
humorous
humorously
humors
hump
humped
humping
humps
hums
hunch
hunchback
hunchbacks
hunched
hunches
hunching
hundred
hundreds
hundredth
hundredths
hung
hunger
hungered
hungering
hungers
hungrier
hungriest
hungrily
hungry
hunk
hunks
hunt
hunted
hunter
hunters
hunting
hunts
hurdle
hurdled
hurdles
hurdling
hurl
hurled
hurling
hurls
hurrah
hurrahed
hurrahing
hurrahs
hurray
hurrayed
hurraying
hurrays
hurricane
hurricanes
hurried
hurriedly
hurries
hurry
hurrying
hurt
hurtful
hurting
hurtle
hurtled
hurtles
hurtling
hurts
husband
husbanded
husbanding
husbands
hush
hushed
hushes
hushing
husk
husked
huskier
huskies
huskiest
huskily
huskiness
husking
husks
husky
hustle
hustled
hustler
hustlers
hustles
hustling
hut
hutch
hutches
huts
hyacinth
hyacinths
hyaena
hyaenas
hybrid
hybrids
hydrant
hydrants
hydraulic
hydraulics
hydroelectric
hydrogen
hydroplane
hydroplaned
hydroplanes
hydroplaning
hyena
hyenas
hygiene
hygienic
hymn
hymnal
hymnals
hymned
hymning
hymns
hyperbole
hypertension
hyphen
hyphenate
hyphenated
hyphenates
hyphenating
hyphenation
hyphened
hyphening
hyphens
hypnosis
hypnotic
hypnotics
hypnotism
hypnotist
hypnotists
hypnotize
hypnotized
hypnotizes
hypnotizing
hypochondria
hypochondriac
hypochondriacs
hypocrisies
hypocrisy
hypocrite
hypocrites
hypocritical
hypotenuse
hypotenuses
hypotheses
hypothesis
hypothesize
hypothesized
hypothesizes
hypothesizing
hypothetical
hysteria
hysteric
hysterical
hysterically
hysterics
ice
iceberg
icebergs
icebreaker
icebreakers
iced
ices
icicle
icicles
icier
iciest
icing
icings
icon
icons
icy
id
idea
ideal
idealist
idealistic
idealists
idealize
idealized
idealizes
idealizing
ideally
ideals
ideas
identical
identically
identifiable
identification
identified
identifier
identifiers
identifies
identify
identifying
identities
identity
ideological
ideologically
ideologies
ideology
idiocies
idiocy
idiom
idiomatic
idioms
idiosyncrasies
idiosyncrasy
idiosyncratic
idiot
idiotic
idiots
idle
idled
idler
idles
idlest
idling
idly
idol
idolize
idolized
idolizes
idolizing
idols
idyllic
if
ifs
igloo
igloos
ignite
ignited
ignites
igniting
ignition
ignitions
ignorance
ignorant
ignore
ignored
ignores
ignoring
iguana
iguanas
ikon
ikons
ilk
ill
illegal
illegally
illegals
illegible
illegibly
illegitimate
illicit
illiteracy
illiterate
illiterates
illness
illnesses
illogical
ills
illuminate
illuminated
illuminates
illuminating
illumination
illuminations
illusion
illusions
illusory
illustrate
illustrated
illustrates
illustrating
illustration
illustrations
illustrative
illustrator
illustrators
illustrious
image
imaged
imagery
images
imaginable
imaginary
imagination
imaginations
imaginative
imagine
imagined
imagines
imaging
imagining
imbalance
imbalances
imbecile
imbeciles
imbed
imbedded
imbedding
imbeds
imitate
imitated
imitates
imitating
imitation
imitations
imitative
imitator
imitators
immaculate
immaculately
immaterial
immature
immaturity
immeasurable
immeasurably
immediate
immediately
immense
immensely
immensities
immensity
immerse
immersed
immerses
immersing
immersion
immersions
immigrant
immigrants
immigrate
immigrated
immigrates
immigrating
immigration
imminent
imminently
immobile
immobilize
immobilized
immobilizes
immobilizing
immoral
immoralities
immorality
immortal
immortality
immortals
immovable
immune
immunity
immunization
immunizations
immunize
immunized
immunizes
immunizing
imp
impact
impacted
impacting
impacts
impair
impaired
impairing
impairment
impairments
impairs
impale
impaled
impales
impaling
impart
imparted
impartial
impartiality
impartially
imparting
imparts
impassable
impasse
impasses
impassioned
impassive
impatience
impatiences
impatient
impatiently
impeach
impeached
impeaches
impeaching
impeccable
impedance
impede
impeded
impedes
impediment
impediments
impeding
impel
impelled
impelling
impels
impend
impended
impending
impends
impenetrable
imperative
imperatives
imperceptible
imperceptibly
imperfect
imperfection
imperfections
imperfectly
imperfects
imperial
imperialism
imperialist
imperials
imperil
imperiled
imperiling
imperilled
imperilling
imperils
impersonal
impersonally
impersonate
impersonated
impersonates
impersonating
impersonation
impersonations
impertinence
impertinent
impervious
impetuous
impetuously
impetus
impetuses
impinge
impinged
impinges
impinging
impish
implacable
implant
implanted
implanting
implants
implausible
implement
implementable
implementation
implementations
implemented
implementer
implementing
implements
implicate
implicated
implicates
implicating
implication
implications
implicit
implicitly
implied
implies
implore
implored
implores
imploring
imply
implying
impolite
import
importance
important
importantly
importation
importations
imported
importing
imports
impose
imposed
imposes
imposing
imposition
impositions
impossibilities
impossibility
impossible
impossibles
impossibly
imposter
imposters
impostor
impostors
impotence
impotent
impound
impounded
impounding
impounds
impoverish
impoverished
impoverishes
impoverishing
impractical
imprecise
impregnable
impregnate
impregnated
impregnates
impregnating
impress
impressed
impresses
impressing
impression
impressionable
impressions
impressive
impressively
imprint
imprinted
imprinting
imprints
imprison
imprisoned
imprisoning
imprisonment
imprisonments
imprisons
improbabilities
improbability
improbable
improbably
impromptu
impromptus
improper
improperly
improprieties
impropriety
improve
improved
improvement
improvements
improves
improving
improvisation
improvisations
improvise
improvised
improvises
improvising
imps
impudence
impudent
impulse
impulsed
impulses
impulsing
impulsive
impulsively
impunity
impure
impurer
impurest
impurities
impurity
in
inabilities
inability
inaccessible
inaccuracies
inaccuracy
inaccurate
inaction
inactive
inactivity
inadequacies
inadequacy
inadequate
inadequately
inadmissible
inadvertent
inadvertently
inadvisable
inalienable
inane
inaner
inanest
inanimate
inapplicable
inappropriate
inarticulate
inasmuch
inaudible
inaugural
inaugurals
inaugurate
inaugurated
inaugurates
inaugurating
inauguration
inaugurations
inauspicious
inborn
inbred
inbreed
inbreeding
inbreeds
inbuilt
incalculable
incandescence
incandescent
incantation
incantations
incapable
incapacitate
incapacitated
incapacitates
incapacitating
incapacity
incarcerate
incarcerated
incarcerates
incarcerating
incarceration
incarcerations
incarnate
incarnated
incarnates
incarnating
incarnation
incarnations
incendiaries
incendiary
incense
incensed
incenses
incensing
incentive
incentives
inception
inceptions
incessant
incessantly
incest
incestuous
inch
inched
inches
inching
incidence
incidences
incident
incidental
incidentally
incidentals
incidents
incinerate
incinerated
incinerates
incinerating
incinerator
incinerators
incision
incisions
incisive
incisor
incisors
incite
incited
incitement
incitements
incites
inciting
inclination
inclinations
incline
inclined
inclines
inclining
inclose
inclosed
incloses
inclosing
inclosure
inclosures
include
included
includes
including
inclusion
inclusions
inclusive
incognito
incognitos
incoherence
incoherent
incoherently
income
incomes
incoming
incomparable
incompatibilities
incompatibility
incompatible
incompatibles
incompatibly
incompetence
incompetent
incompetents
incomplete
incomprehensible
inconceivable
inconclusive
incongruities
incongruity
incongruous
inconsequential
inconsiderable
inconsiderate
inconsistencies
inconsistency
inconsistent
inconsolable
inconspicuous
inconvenience
inconvenienced
inconveniences
inconveniencing
inconvenient
inconveniently
incorporate
incorporated
incorporates
incorporating
incorporation
incorrect
incorrectly
incorrigible
increase
increased
increases
increasing
increasingly
incredible
incredibly
incredulity
incredulous
increment
incremental
incremented
increments
incriminate
incriminated
incriminates
incriminating
incubate
incubated
incubates
incubating
incubation
incubator
incubators
incumbent
incumbents
incur
incurable
incurables
incurred
incurring
incurs
indebted
indecencies
indecency
indecent
indecision
indecisive
indeed
indefensible
indefinable
indefinite
indefinitely
indelible
indelibly
indelicate
indent
indentation
indentations
indented
indenting
indents
independence
independent
independently
independents
indescribable
indestructible
indeterminate
index
indexed
indexes
indexing
indicate
indicated
indicates
indicating
indication
indications
indicative
indicatives
indicator
indicators
indices
indict
indicted
indicting
indictment
indictments
indicts
indifference
indifferent
indigenous
indigestible
indigestion
indignant
indignantly
indignation
indignities
indignity
indigo
indirect
indirection
indirectly
indiscreet
indiscretion
indiscretions
indiscriminate
indiscriminately
indispensable
indispensables
indisposed
indisputable
indistinct
indistinguishable
individual
individualism
individualist
individualists
individuality
individually
individuals
indivisible
indoctrinate
indoctrinated
indoctrinates
indoctrinating
indoctrination
indolence
indolent
indomitable
indoor
indoors
indorse
indorsed
indorsement
indorsements
indorses
indorsing
induce
induced
inducement
inducements
induces
inducing
induct
inducted
inducting
induction
inductions
inducts
indulge
indulged
indulgence
indulgences
indulgent
indulges
indulging
industrial
industrialist
industrialists
industrialization
industrialize
industrialized
industrializes
industrializing
industries
industrious
industry
inedible
ineffective
ineffectual
inefficiencies
inefficiency
inefficient
inefficiently
inelegant
ineligible
ineligibles
inept
ineptitude
inequalities
inequality
inert
inertia
inertial
inescapable
inevitable
inevitably
inexact
inexcusable
inexhaustible
inexorable
inexorably
inexpensive
inexperience
inexperienced
inexplicable
inexplicably
inextricably
infallible
infamies
infamous
infamy
infancy
infant
infantile
infantries
infantry
infants
infatuation
infatuations
infect
infected
infecting
infection
infections
infectious
infects
infelicities
infelicity
infer
inference
inferences
inferior
inferiority
inferiors
inferno
infernos
inferred
inferring
infers
infertile
infest
infestation
infestations
infested
infesting
infests
infidel
infidelities
infidelity
infidels
infield
infields
infiltrate
infiltrated
infiltrates
infiltrating
infiltration
infinite
infinitely
infinitesimal
infinitesimals
infinities
infinitive
infinitives
infinity
infirm
infirmaries
infirmary
infirmities
infirmity
infix
inflame
inflamed
inflames
inflaming
inflammable
inflammation
inflammations
inflammatory
inflatable
inflate
inflated
inflates
inflating
inflation
inflationary
inflection
inflections
inflexible
inflict
inflicted
inflicting
inflicts
influence
influenced
influences
influencing
influential
influenza
influx
influxes
info
inform
informal
informality
informally
informant
informants
information
informational
informative
informed
informer
informers
informing
informs
infraction
infractions
infrared
infrastructure
infrequent
infrequently
infringe
infringed
infringement
infringements
infringes
infringing
infuriate
infuriated
infuriates
infuriating
infuse
infused
infuses
infusing
infusion
infusions
ingenious
ingeniously
ingenuity
ingest
ingested
ingesting
ingests
ingrain
ingrained
ingraining
ingrains
ingratiate
ingratiated
ingratiates
ingratiating
ingratitude
ingredient
ingredients
inhabit
inhabitant
inhabitants
inhabited
inhabiting
inhabits
inhale
inhaled
inhaler
inhalers
inhales
inhaling
inherent
inherently
inherit
inheritance
inheritances
inherited
inheriting
inherits
inhibit
inhibited
inhibiting
inhibition
inhibitions
inhibits
inhospitable
inhuman
inhumane
inhumanities
inhumanity
initial
initialed
initialing
initialization
initialize
initialized
initializes
initializing
initialled
initialling
initially
initials
initiate
initiated
initiates
initiating
initiation
initiations
initiative
initiatives
initiator
initiators
inject
injected
injecting
injection
injections
injects
injunction
injunctions
injure
injured
injures
injuries
injuring
injurious
injury
injustice
injustices
ink
inked
inkier
inkiest
inking
inkling
inklings
inks
inky
inlaid
inland
inlay
inlaying
inlays
inlet
inlets
inmate
inmates
inn
innards
innate
inner
innermost
inning
innings
innkeeper
innkeepers
innocence
innocent
innocently
innocents
innocuous
innovation
innovations
innovative
inns
innuendo
innuendoes
innuendos
innumerable
inoculate
inoculated
inoculates
inoculating
inoculation
inoculations
inoffensive
inoperative
inopportune
inordinate
input
inputs
inputted
inputting
inquest
inquests
inquire
inquired
inquires
inquiries
inquiring
inquiry
inquisition
inquisitions
inquisitive
ins
insane
insanely
insaner
insanest
insanity
insatiable
inscribe
inscribed
inscribes
inscribing
inscription
inscriptions
inscrutable
insect
insecticide
insecticides
insects
insecure
insecurities
insecurity
insensitive
insensitivity
inseparable
inseparables
insert
inserted
inserting
insertion
insertions
inserts
inside
insider
insiders
insides
insidious
insight
insights
insigne
insignes
insignia
insignias
insignificance
insignificant
insincere
insincerely
insincerity
insinuate
insinuated
insinuates
insinuating
insinuation
insinuations
insipid
insist
insisted
insistence
insistent
insisting
insists
insofar
insolence
insolent
insoluble
insolvency
insolvent
insolvents
insomnia
inspect
inspected
inspecting
inspection
inspections
inspector
inspectors
inspects
inspiration
inspirations
inspire
inspired
inspires
inspiring
instability
instal
install
installation
installations
installed
installing
installment
installments
installs
instalment
instalments
instals
instance
instanced
instances
instancing
instant
instantaneous
instantaneously
instantly
instants
instead
instep
insteps
instigate
instigated
instigates
instigating
instigation
instil
instill
instilled
instilling
instills
instils
instinct
instinctive
instincts
institute
instituted
institutes
instituting
institution
institutional
institutionalize
institutionalized
institutionalizes
institutionalizing
institutions
instruct
instructed
instructing
instruction
instructions
instructive
instructor
instructors
instructs
instrument
instrumental
instrumentals
instrumented
instrumenting
instruments
insubordinate
insubordination
insubstantial
insufferable
insufficient
insufficiently
insular
insulate
insulated
insulates
insulating
insulation
insulator
insulators
insulin
insult
insulted
insulting
insults
insurance
insurances
insure
insured
insurer
insurers
insures
insurgent
insurgents
insuring
insurmountable
insurrection
insurrections
intact
intake
intakes
intangible
intangibles
integer
integers
integral
integrals
integrate
integrated
integrates
integrating
integration
integrity
intellect
intellects
intellectual
intellectually
intellectuals
intelligence
intelligent
intelligently
intelligible
intelligibly
intend
intended
intending
intends
intense
intensely
intenser
intensest
intensified
intensifies
intensify
intensifying
intensities
intensity
intensive
intensives
intent
intention
intentional
intentionally
intentions
intents
inter
interact
interacted
interacting
interaction
interactions
interactive
interactively
interacts
intercede
interceded
intercedes
interceding
intercept
intercepted
intercepting
interception
interceptions
intercepts
interchange
interchangeable
interchanged
interchanges
interchanging
intercom
intercoms
interconnect
intercontinental
intercourse
interdependence
interdependent
interest
interested
interesting
interestingly
interests
interface
interfaced
interfaces
interfacing
interfere
interfered
interference
interferes
interfering
interim
interior
interiors
interject
interjected
interjecting
interjection
interjections
interjects
interlock
interlocked
interlocking
interlocks
interloper
interlopers
interlude
interluded
interludes
interluding
intermarriage
intermarriages
intermarried
intermarries
intermarry
intermarrying
intermediaries
intermediary
intermediate
intermediates
interment
interments
interminable
interminably
intermingle
intermingled
intermingles
intermingling
intermission
intermissions
intermittent
intermittently
intern
internal
internally
internals
international
internationally
internationals
interne
interned
internes
internet
interning
interns
interplanetary
interplay
interpolation
interpose
interposed
interposes
interposing
interpret
interpretation
interpretations
interpreted
interpreter
interpreters
interpreting
interprets
interracial
interred
interring
interrogate
interrogated
interrogates
interrogating
interrogation
interrogations
interrogator
interrogators
interrupt
interrupted
interrupting
interruption
interruptions
interrupts
inters
intersect
intersected
intersecting
intersection
intersections
intersects
intersperse
interspersed
intersperses
interspersing
interstate
interstates
interstellar
intertwine
intertwined
intertwines
intertwining
interval
intervals
intervene
intervened
intervenes
intervening
intervention
interventions
interview
interviewed
interviewer
interviewers
interviewing
interviews
interweave
interweaved
interweaves
interweaving
interwove
interwoven
intestinal
intestine
intestines
intimacies
intimacy
intimate
intimated
intimately
intimates
intimating
intimation
intimations
intimidate
intimidated
intimidates
intimidating
intimidation
into
intolerable
intolerably
intolerance
intolerant
intonation
intonations
intoxicate
intoxicated
intoxicates
intoxicating
intoxication
intractable
intramural
intransitive
intransitives
intravenous
intravenouses
intrench
intrenched
intrenches
intrenching
intrepid
intricacies
intricacy
intricate
intrigue
intrigued
intrigues
intriguing
intrinsic
intrinsically
introduce
introduced
introduces
introducing
introduction
introductions
introductory
introspective
introvert
introverts
intrude
intruded
intruder
intruders
intrudes
intruding
intrusion
intrusions
intrusive
intrust
intrusted
intrusting
intrusts
intuition
intuitions
intuitive
intuitively
inundate
inundated
inundates
inundating
inundation
inundations
invade
invaded
invader
invaders
invades
invading
invalid
invalidate
invalidated
invalidates
invalidating
invalided
invaliding
invalids
invaluable
invariable
invariables
invariably
invariant
invasion
invasions
invective
invent
invented
inventing
invention
inventions
inventive
inventor
inventoried
inventories
inventors
inventory
inventorying
invents
inverse
inversely
inverses
inversion
inversions
invert
invertebrate
invertebrates
inverted
inverting
inverts
invest
invested
investigate
investigated
investigates
investigating
investigation
investigations
investigator
investigators
investing
investment
investments
investor
investors
invests
inveterate
invigorate
invigorated
invigorates
invigorating
invincible
invisibility
invisible
invisibly
invitation
invitations
invite
invited
invites
inviting
invocation
invocations
invoice
invoiced
invoices
invoicing
invoke
invoked
invokes
invoking
involuntarily
involuntary
involve
involved
involvement
involvements
involves
involving
invulnerable
inward
inwardly
inwards
iodine
ion
ions
iota
iotas
irascible
irate
ire
iridescence
iridescent
iris
irises
irk
irked
irking
irks
iron
ironed
ironic
ironically
ironies
ironing
irons
irony
irradiate
irradiated
irradiates
irradiating
irrational
irrationally
irrationals
irreconcilable
irrefutable
irregular
irregularities
irregularity
irregulars
irrelevance
irrelevances
irrelevant
irreparable
irreplaceable
irrepressible
irreproachable
irresistible
irrespective
irresponsibility
irresponsible
irretrievable
irretrievably
irreverence
irreverent
irreversible
irrevocable
irrevocably
irrigate
irrigated
irrigates
irrigating
irrigation
irritability
irritable
irritably
irritant
irritants
irritate
irritated
irritates
irritating
irritation
irritations
is
island
islander
islanders
islands
isle
isles
isolate
isolated
isolates
isolating
isolation
issue
issued
issues
issuing
isthmi
isthmus
isthmuses
it
italic
italicize
italicized
italicizes
italicizing
italics
itch
itched
itches
itchier
itchiest
itching
itchy
item
itemize
itemized
itemizes
itemizing
items
iterate
iteration
iterations
iterative
itinerant
itinerants
itineraries
itinerary
its
itself
ivies
ivories
ivory
ivy
jab
jabbed
jabber
jabbered
jabbering
jabbers
jabbing
jabs
jack
jackal
jackals
jackass
jackasses
jackdaw
jacked
jacket
jackets
jacking
jackknife
jackknifed
jackknifes
jackknifing
jackknives
jackpot
jackpots
jacks
jade
jaded
jades
jading
jagged
jaggeder
jaggedest
jaguar
jaguars
jail
jailed
jailer
jailers
jailing
jailor
jailors
jails
jalopies
jalopy
jam
jamb
jamboree
jamborees
jambs
jammed
jamming
jams
jangle
jangled
jangles
jangling
janitor
janitors
jar
jargon
jarred
jarring
jars
jaundice
jaundiced
jaundices
jaundicing
jaunt
jaunted
jauntier
jauntiest
jauntily
jaunting
jaunts
jaunty
javelin
javelins
jaw
jawbone
jawboned
jawbones
jawboning
jawed
jawing
jaws
jay
jays
jaywalk
jaywalked
jaywalker
jaywalkers
jaywalking
jaywalks
jazz
jazzed
jazzes
jazzing
jealous
jealousies
jealously
jealousy
jeans
jeer
jeered
jeering
jeers
jell
jelled
jellied
jellies
jelling
jells
jelly
jellyfish
jellyfishes
jellying
jeopardize
jeopardized
jeopardizes
jeopardizing
jeopardy
jerk
jerked
jerkier
jerkiest
jerking
jerks
jerky
jersey
jerseys
jest
jested
jester
jesters
jesting
jests
jet
jets
jetted
jetties
jetting
jettison
jettisoned
jettisoning
jettisons
jetty
jewel
jeweled
jeweler
jewelers
jeweling
jewelled
jeweller
jewellers
jewelling
jewelries
jewelry
jewels
jibe
jibed
jibes
jibing
jiffies
jiffy
jig
jigged
jigging
jiggle
jiggled
jiggles
jiggling
jigs
jigsaw
jigsawed
jigsawing
jigsawn
jigsaws
jilt
jilted
jilting
jilts
jingle
jingled
jingles
jingling
jinx
jinxed
jinxes
jinxing
jitterier
jitteriest
jitters
jittery
job
jobbed
jobbing
jobs
jockey
jockeyed
jockeying
jockeys
jocular
jog
jogged
jogger
joggers
jogging
jogs
join
joined
joining
joins
joint
jointed
jointing
jointly
joints
joke
joked
joker
jokers
jokes
joking
jollied
jollier
jollies
jolliest
jolly
jollying
jolt
jolted
jolting
jolts
jostle
jostled
jostles
jostling
jot
jots
jotted
jotting
journal
journalism
journalist
journalists
journals
journey
journeyed
journeying
journeys
jovial
jovially
joy
joyed
joyful
joyfuller
joyfullest
joyfully
joying
joyous
joyously
joys
joystick
jubilant
jubilation
jubilee
jubilees
judge
judged
judgement
judgements
judges
judging
judgment
judgments
judicial
judicially
judiciaries
judiciary
judicious
judiciously
judo
jug
jugged
juggernaut
jugging
juggle
juggled
juggler
jugglers
juggles
juggling
jugs
jugular
jugulars
juice
juiced
juices
juicier
juiciest
juicing
juicy
jumble
jumbled
jumbles
jumbling
jumbo
jumbos
jump
jumped
jumper
jumpers
jumpier
jumpiest
jumping
jumps
jumpy
junction
junctions
juncture
junctures
jungle
jungles
junior
juniors
juniper
junipers
junk
junked
junket
junketed
junketing
junkets
junkie
junkies
junking
junks
junky
junta
juntas
juries
jurisdiction
juror
jurors
jury
just
juster
justest
justice
justices
justifiable
justifiably
justification
justifications
justified
justifies
justify
justifying
justly
jut
jute
juts
jutted
jutting
juvenile
juveniles
juxtapose
juxtaposed
juxtaposes
juxtaposing
juxtaposition
juxtapositions
kaleidoscope
kaleidoscopes
kangaroo
kangaroos
karat
karate
karats
kayak
kayaked
kayaking
kayaks
keel
keeled
keeling
keels
keen
keened
keener
keenest
keening
keenly
keens
keep
keeper
keepers
keeping
keeps
keepsake
keepsakes
keg
kegs
kelp
ken
kennel
kenneled
kenneling
kennelled
kennelling
kennels
kept
kerchief
kerchiefs
kerchieves
kernel
kernels
kerosene
kerosine
ketchup
kettle
kettles
key
keyboard
keyboarded
keyboarding
keyboards
keyed
keyhole
keyholes
keying
keynote
keynoted
keynotes
keynoting
keys
keystone
keystones
keystroke
keystrokes
keyword
keywords
khaki
khakis
kick
kickback
kickbacks
kicked
kicking
kickoff
kickoffs
kicks
kid
kidded
kidding
kidnap
kidnaped
kidnaper
kidnapers
kidnaping
kidnapped
kidnapper
kidnappers
kidnapping
kidnaps
kidney
kidneys
kids
kill
killed
killer
killers
killing
killings
kills
kiln
kilned
kilning
kilns
kilo
kilobyte
kilobytes
kilogram
kilograms
kilometer
kilometers
kilos
kilowatt
kilowatts
kilt
kilts
kimono
kimonos
kin
kind
kinda
kinder
kindergarten
kindergartens
kindest
kindle
kindled
kindles
kindlier
kindliest
kindling
kindly
kindness
kindnesses
kindred
kinds
kinfolk
king
kingdom
kingdoms
kingfisher
kingfishers
kings
kink
kinked
kinkier
kinkiest
kinking
kinks
kinky
kinship
kiosk
kiosks
kipper
kiss
kissed
kisses
kissing
kit
kitchen
kitchenette
kitchenettes
kitchens
kite
kited
kites
kiting
kits
kitten
kittens
kitties
kitty
kiwi
kiwis
knack
knacker
knacks
knapsack
knapsacks
knead
kneaded
kneading
kneads
knee
kneecap
kneecapped
kneecapping
kneecaps
kneed
kneeing
kneel
kneeled
kneeling
kneels
knees
knelt
knew
knickers
knife
knifed
knifes
knifing
knight
knighted
knighthood
knighthoods
knighting
knights
knit
knits
knitted
knitting
knives
knob
knobs
knock
knocked
knocker
knockers
knocking
knockout
knockouts
knocks
knoll
knolls
knot
knots
knotted
knottier
knottiest
knotting
knotty
know
knowing
knowingly
knowings
knowledge
knowledgeable
known
knows
knuckle
knuckled
knuckles
knuckling
koala
koalas
kosher
koshered
koshering
koshers
kowtow
kowtowed
kowtowing
kowtows
kudos
lab
label
labeled
labeling
labelled
labelling
labels
labor
laboratories
laboratory
labored
laborer
laborers
laboring
laborious
laboriously
labors
labs
labyrinth
labyrinths
lace
laced
lacerate
lacerated
lacerates
lacerating
laceration
lacerations
laces
lacier
laciest
lacing
lack
lacked
lacking
lackluster
lacks
lacquer
lacquered
lacquering
lacquers
lacrosse
lacy
lad
ladder
laddered
laddering
ladders
lade
laded
laden
lades
ladies
lading
ladle
ladled
ladles
ladling
lads
lady
ladybug
ladybugs
ladylike
lag
lager
laggard
laggards
lagged
lagging
lagoon
lagoons
lags
laid
lain
lair
lairs
lake
lakes
lamb
lambda
lambed
lambing
lambs
lame
lamed
lament
lamentable
lamentation
lamentations
lamented
lamenting
laments
lamer
lames
lamest
laming
lamp
lampoon
lampooned
lampooning
lampoons
lamps
lance
lanced
lances
lancing
land
landed
lander
landing
landings
landladies
landlady
landlocked
landlord
landlords
landmark
landmarks
landowner
landowners
lands
landscape
landscaped
landscapes
landscaping
landslid
landslidden
landslide
landslides
landsliding
lane
lanes
language
languages
languid
languish
languished
languishes
languishing
languor
languorous
languors
lankier
lankiest
lanky
lantern
lanterns
lap
lapel
lapels
lapped
lapping
laps
lapse
lapsed
lapses
lapsing
larcenies
larceny
lard
larded
larding
lards
large
largely
larger
larges
largest
lark
larked
larking
larks
larva
larvae
larvas
larynges
laryngitis
larynx
larynxes
lascivious
laser
lasers
lash
lashed
lashes
lashing
lass
lasses
last
lasted
lasting
lastly
lasts
latch
latched
latches
latching
late
lately
latent
later
lateral
lateraled
lateraling
lateralled
lateralling
laterals
latest
latex
lath
lathe
lathed
lather
lathered
lathering
lathers
lathes
lathing
laths
latitude
latitudes
latrine
latrines
latter
lattice
lattices
laud
laudable
lauded
lauding
lauds
laugh
laughable
laughed
laughing
laughingstock
laughingstocks
laughs
laughter
launch
launched
launcher
launchers
launches
launching
launder
laundered
laundering
launders
laundries
laundry
laureate
laureates
laurel
laurels
lava
lavatories
lavatory
lavender
lavenders
lavish
lavished
lavisher
lavishes
lavishest
lavishing
law
lawful
lawless
lawmaker
lawmakers
lawn
lawns
laws
lawsuit
lawsuits
lawyer
lawyers
lax
laxative
laxatives
laxer
laxest
laxity
lay
layer
layered
layering
layers
laying
layman
laymen
layout
layouts
lays
lazied
lazier
lazies
laziest
laziness
lazy
lazying
leach
lead
leaded
leaden
leader
leaders
leadership
leading
leads
leaf
leafed
leafier
leafiest
leafing
leaflet
leafleted
leafleting
leaflets
leafletted
leafletting
leafs
leafy
league
leagued
leagues
leaguing
leak
leakage
leakages
leaked
leaking
leaks
leaky
lean
leaned
leaner
leanest
leaning
leans
leap
leaped
leapfrog
leapfrogged
leapfrogging
leapfrogs
leaping
leaps
leapt
learn
learned
learning
learns
learnt
lease
leased
leases
leash
leashed
leashes
leashing
leasing
least
leather
leathery
leave
leaved
leaves
leaving
lectern
lecterns
lecture
lectured
lecturer
lecturers
lectures
lecturing
led
ledge
ledger
ledgers
ledges
lee
leech
leeched
leeches
leeching
leek
leeks
leer
leered
leerier
leeriest
leering
leers
leery
leeway
left
lefter
leftest
leftmost
lefts
leg
legacies
legacy
legal
legalistic
legality
legalize
legalized
legalizes
legalizing
legally
legals
legend
legendary
legends
legged
leggin
legging
leggings
leggins
legibility
legible
legibly
legion
legions
legislate
legislated
legislates
legislating
legislation
legislative
legislator
legislators
legislature
legislatures
legitimacy
legitimate
legitimated
legitimately
legitimates
legitimating
legs
legume
legumes
leisure
leisurely
lemme
lemon
lemonade
lemons
lend
lending
lends
length
lengthen
lengthened
lengthening
lengthens
lengthier
lengthiest
lengths
lengthwise
lengthy
leniency
lenient
lens
lenses
lent
lentil
lentils
leopard
leopards
leotard
leotards
leper
lepers
leprosy
lept
lesbian
lesbians
lesion
lesions
less
lessen
lessened
lessening
lessens
lesser
lesson
lessons
lest
let
letdown
letdowns
lethal
lethargic
lethargy
lets
letter
lettered
letterhead
letterheads
lettering
letters
letting
lettuce
lettuces
letup
letups
leukemia
levee
levees
level
leveled
leveling
levelled
levelling
levels
lever
leverage
leveraged
leverages
leveraging
levered
levering
levers
levied
levies
levity
levy
levying
lewd
lewder
lewdest
lexica
lexical
lexicon
lexicons
liabilities
liability
liable
liaison
liaisons
liar
liars
libel
libeled
libeling
libelled
libelling
libellous
libelous
libels
liberal
liberalism
liberalization
liberalize
liberalized
liberalizes
liberalizing
liberally
liberals
liberate
liberated
liberates
liberating
liberation
libertarian
liberties
liberty
librarian
librarians
libraries
library
libretto
lice
licence
licenced
licences
licencing
license
licensed
licenses
licensing
lichen
lichens
lick
licked
licking
licks
licorice
licorices
lid
lids
lie
lied
lies
lieu
lieutenant
lieutenants
life
lifeboat
lifeboats
lifeforms
lifeguard
lifeguards
lifeless
lifelike
lifeline
lifelines
lifelong
lifespan
lifestyle
lifestyles
lifetime
lifetimes
lift
lifted
lifting
lifts
ligament
ligaments
ligature
ligatures
light
lighted
lighten
lightened
lightening
lightens
lighter
lighters
lightest
lighthouse
lighthouses
lighting
lightly
lightness
lightning
lightninged
lightnings
lights
lightweight
lightweights
likable
like
likeable
liked
likelier
likeliest
likelihood
likelihoods
likely
liken
likened
likeness
likenesses
likening
likens
liker
likes
likest
likewise
liking
lilac
lilacs
lilies
lilt
lilted
lilting
lilts
lily
limb
limber
limbered
limbering
limbers
limbo
limbs
lime
limed
limelight
limerick
limericks
limes
limestone
liming
limit
limitation
limitations
limited
limiting
limitless
limits
limousine
limousines
limp
limped
limper
limpest
limping
limps
linchpin
linchpins
line
lineage
lineages
linear
linearly
lined
linefeed
linen
liner
liners
lines
linger
lingered
lingerie
lingering
lingers
lingo
lingoes
lingos
linguist
linguistic
linguistics
linguists
liniment
liniments
lining
linings
link
linkage
linked
linker
linking
links
linoleum
lint
lion
lioness
lionesses
lions
lip
lips
lipstick
lipsticked
lipsticking
lipsticks
liquefied
liquefies
liquefy
liquefying
liqueur
liqueurs
liquid
liquidate
liquidated
liquidates
liquidating
liquidation
liquidations
liquids
liquified
liquifies
liquify
liquifying
liquor
liquored
liquoring
liquors
lisp
lisped
lisping
lisps
list
listed
listen
listened
listener
listeners
listening
listens
listing
listings
listless
lists
lit
litanies
litany
liter
literacy
literal
literally
literals
literary
literate
literates
literature
liters
lithe
lither
lithest
lithium
litigation
litter
litterbug
litterbugs
littered
littering
litters
little
littler
littlest
liturgical
liturgies
liturgy
livable
live
liveable
lived
livelier
liveliest
livelihood
livelihoods
liveliness
lively
liven
livened
livening
livens
liver
livers
lives
livest
livestock
livid
living
livings
lizard
lizards
llama
llamas
load
loadable
loaded
loader
loading
loads
loaf
loafed
loafer
loafers
loafing
loafs
loam
loan
loaned
loaning
loans
loath
loathe
loathed
loathes
loathing
loathings
loathsome
loaves
lob
lobbed
lobbied
lobbies
lobbing
lobby
lobbying
lobbyist
lobbyists
lobe
lobes
lobotomy
lobs
lobster
lobsters
local
locale
locales
localities
locality
localize
localized
localizes
localizing
locally
locals
locate
located
locates
locating
location
locations
lock
locked
locker
lockers
locket
lockets
locking
locks
locksmith
locksmiths
locomotion
locomotive
locomotives
locust
locusts
lodge
lodged
lodger
lodgers
lodges
lodging
lodgings
loft
lofted
loftier
loftiest
loftiness
lofting
lofts
lofty
log
logarithm
logarithmic
logged
logger
logging
logic
logical
logically
logician
logo
logs
loin
loincloth
loincloths
loins
loiter
loitered
loiterer
loiterers
loitering
loiters
loll
lolled
lolling
lollipop
lollipops
lolls
lollypop
lollypops
lone
lonelier
loneliest
loneliness
lonely
lonesome
long
longed
longer
longest
longevity
longhand
longing
longings
longish
longitude
longitudes
longitudinal
longs
longshoreman
longshoremen
look
looked
looking
lookout
lookouts
looks
loom
loomed
looming
looms
loon
looney
looneyier
looneyies
looneys
loonier
loonies
looniest
loons
loony
loop
looped
loophole
loopholes
looping
loops
loose
loosed
loosely
loosen
loosened
loosening
loosens
looser
looses
loosest
loosing
loot
looted
looting
loots
lop
lope
loped
lopes
loping
lopped
lopping
lops
lopsided
lord
lorded
lording
lords
lore
lorries
lorry
lose
loser
losers
loses
losing
loss
losses
lost
lot
loth
lotion
lotions
lots
lotteries
lottery
lotus
lotuses
loud
louder
loudest
loudly
loudness
loudspeaker
loudspeakers
lounge
lounged
lounges
lounging
louse
louses
lousier
lousiest
lousy
lovable
love
loveable
loved
lovelier
lovelies
loveliest
loveliness
lovely
lover
lovers
loves
loving
lovingly
low
lowdown
lowed
lower
lowered
lowering
lowers
lowest
lowing
lowlier
lowliest
lowly
lows
loyal
loyaler
loyalest
loyaller
loyallest
loyalties
loyalty
lozenge
lozenges
lubricant
lubricants
lubricate
lubricated
lubricates
lubricating
lubrication
lucid
luck
lucked
luckier
luckiest
luckily
lucking
lucks
lucky
lucrative
ludicrous
ludicrously
lug
luggage
lugged
lugging
lugs
lukewarm
lull
lullabies
lullaby
lulled
lulling
lulls
lumber
lumbered
lumbering
lumberjack
lumberjacks
lumbers
luminaries
luminary
luminous
lump
lumped
lumpier
lumpiest
lumping
lumps
lumpy
lunacies
lunacy
lunar
lunatic
lunatics
lunch
lunched
luncheon
luncheons
lunches
lunching
lunchtime
lung
lunge
lunged
lunges
lunging
lungs
lupin
lupins
lurch
lurched
lurches
lurching
lure
lured
lures
lurid
luring
lurk
lurked
lurking
lurks
luscious
lush
lusher
lushes
lushest
lust
lusted
luster
lustier
lustiest
lusting
lustre
lustrous
lusts
lusty
lute
lutes
luxuriant
luxuriate
luxuriated
luxuriates
luxuriating
luxuries
luxurious
luxury
lye
lying
lymph
lymphatic
lymphatics
lynch
lynched
lynches
lynching
lynchpin
lynchpins
lyre
lyres
lyric
lyrical
lyrics
m
ma
macabre
macaroni
macaronies
macaronis
mace
maced
maces
machete
machetes
machine
machined
machinery
machines
machining
machinist
machinists
macho
macing
macintosh
mackerel
mackerels
macroscopic
mad
madam
madame
madams
madcap
madcaps
madden
maddened
maddening
maddens
madder
maddest
made
madhouse
madhouses
madly
madman
madmen
madness
mads
maelstrom
maelstroms
magazine
magazines
magenta
maggot
maggots
magic
magical
magically
magician
magicians
magistrate
magistrates
magnanimity
magnanimous
magnanimously
magnate
magnates
magnesium
magnet
magnetic
magnetism
magnetize
magnetized
magnetizes
magnetizing
magnets
magnificence
magnificent
magnified
magnifies
magnify
magnifying
magnitude
magnitudes
magnolia
magnolias
magnum
magpie
magpies
mahoganies
mahogany
maid
maiden
maidens
maids
mail
mailbox
mailboxes
mailed
mailing
mailman
mailmen
mails
maim
maimed
maiming
maims
main
mainframe
mainframes
mainland
mainlands
mainline
mainly
mains
mainstay
mainstays
mainstream
maintain
maintainability
maintainable
maintained
maintainer
maintainers
maintaining
maintains
maintenance
maize
maizes
majestic
majestically
majesties
majesty
major
majored
majoring
majorities
majority
majors
make
maker
makers
makes
makeshift
makeshifts
makeup
makeups
making
maladies
maladjusted
malady
malaria
male
males
malevolence
malevolent
malformed
malfunction
malice
malicious
maliciously
malign
malignancies
malignancy
malignant
maligned
maligning
maligns
mall
mallard
mallards
malleable
mallet
mallets
malls
malnutrition
malpractice
malpractices
malt
malted
malting
maltreat
maltreated
maltreating
maltreats
malts
mama
mamas
mamma
mammal
mammalian
mammals
mammas
mammoth
mammoths
man
manacle
manacled
manacles
manacling
manage
manageable
managed
management
manager
managerial
managers
manages
managing
mandate
mandated
mandates
mandating
mandatory
mandible
mandibles
mandolin
mandolins
mane
manes
maneuver
maneuvered
maneuvering
maneuvers
mange
manger
mangers
mangier
mangiest
mangle
mangled
mangles
mangling
mango
mangoes
mangos
mangrove
mangroves
mangy
manhandle
manhandled
manhandles
manhandling
manhole
manholes
manhood
mania
maniac
maniacal
maniacs
manias
manic
manicure
manicured
manicures
manicuring
manicurist
manicurists
manifest
manifestation
manifestations
manifested
manifesting
manifestly
manifesto
manifestoes
manifestos
manifests
manifold
manifolded
manifolding
manifolds
manipulate
manipulated
manipulates
manipulating
manipulation
manipulations
mankind
manlier
manliest
manliness
manly
manned
mannequin
mannequins
manner
mannerism
mannerisms
manners
manning
mannish
manor
manors
manpower
mans
mansion
mansions
manslaughter
mantel
mantelpiece
mantelpieces
mantels
mantle
mantled
mantlepiece
mantlepieces
mantles
mantling
manual
manually
manuals
manufacture
manufactured
manufacturer
manufacturers
manufactures
manufacturing
manure
manured
manures
manuring
manuscript
manuscripts
many
map
maple
maples
mapped
mapper
mapping
mappings
maps
mar
marathon
marathons
marble
marbled
marbles
marbling
march
marched
marcher
marches
marching
mare
mares
margarine
margin
marginal
marginally
margins
maria
marigold
marigolds
marihuana
marijuana
marina
marinas
marinate
marinated
marinates
marinating
marine
mariner
mariners
marines
marionette
marionettes
marital
maritime
mark
marked
markedly
marker
markers
market
marketable
marketed
marketing
marketplace
marketplaces
markets
marking
markings
marks
marksman
marksmen
marmalade
maroon
marooned
marooning
maroons
marquee
marquees
marred
marriage
marriages
married
marries
marring
marrow
marrows
marry
marrying
mars
marsh
marshal
marshaled
marshaling
marshalled
marshalling
marshals
marshes
marshier
marshiest
marshmallow
marshmallows
marshy
marsupial
marsupials
mart
martial
martin
marts
martyr
martyrdom
martyred
martyring
martyrs
marvel
marveled
marveling
marvelled
marvelling
marvelous
marvels
mas
mascara
mascaraed
mascaraing
mascaras
mascot
mascots
masculine
masculines
mash
mashed
mashes
mashing
mask
masked
masking
masks
masochist
masochists
mason
masonry
masons
masquerade
masqueraded
masquerades
masquerading
mass
massacre
massacred
massacres
massacring
massage
massaged
massages
massaging
massed
masses
massing
massive
massively
mast
master
mastered
masterful
mastering
masterly
mastermind
masterminded
masterminding
masterminds
masterpiece
masterpieces
masters
mastery
masticate
masticated
masticates
masticating
masts
masturbation
mat
matador
matadors
match
matchbook
matchbooks
matched
matches
matching
matchless
matchmaker
matchmakers
mate
mated
material
materialism
materialist
materialistic
materialists
materialize
materialized
materializes
materializing
materials
maternal
maternity
mates
math
mathematical
mathematically
mathematician
mathematicians
mathematics
mating
matriarch
matriarchal
matriarchs
matrices
matriculate
matriculated
matriculates
matriculating
matriculation
matrimonial
matrimony
matrix
matrixes
matron
matronly
matrons
mats
matt
matte
matted
matter
mattered
mattering
matters
mattes
matting
mattress
mattresses
matts
mature
matured
maturer
matures
maturest
maturing
maturities
maturity
maudlin
maul
mauled
mauling
mauls
mausolea
mausoleum
mausoleums
mauve
maverick
mavericks
maxim
maxima
maximal
maximize
maximized
maximizes
maximizing
maxims
maximum
maximums
may
maybe
maybes
mayhem
mayonnaise
mayor
mayors
maze
mazes
me
meadow
meadows
meager
meal
mealier
mealiest
meals
mealy
mean
meander
meandered
meandering
meanders
meaner
meanest
meaning
meaningful
meaningless
meanings
means
meant
meantime
meanwhile
measles
measlier
measliest
measly
measurable
measure
measured
measurement
measurements
measures
measuring
meat
meats
mechanic
mechanical
mechanically
mechanics
mechanism
mechanisms
mechanize
mechanized
mechanizes
mechanizing
medal
medallion
medallions
medals
meddle
meddled
meddler
meddlers
meddles
meddlesome
meddling
media
mediaeval
median
medias
mediate
mediated
mediates
mediating
mediation
mediator
mediators
medical
medically
medicals
medicate
medicated
medicates
medicating
medication
medications
medicinal
medicine
medicines
medieval
mediocre
mediocrities
mediocrity
meditate
meditated
meditates
meditating
meditation
meditations
medium
mediums
medley
medleys
meek
meeker
meekest
meekly
meekness
meet
meeting
meetings
meets
megabyte
megabytes
megalomaniac
megaphone
megaphoned
megaphones
megaphoning
megaton
megatons
melancholy
mellow
mellowed
mellower
mellowest
mellowing
mellows
melodic
melodies
melodious
melodrama
melodramas
melodramatic
melody
melon
melons
melt
melted
melting
melts
member
members
membership
memberships
membrane
membranes
memento
mementoes
mementos
memo
memoir
memoirs
memorable
memorably
memoranda
memorandum
memorandums
memorial
memorials
memories
memorize
memorized
memorizes
memorizing
memory
memos
men
menace
menaced
menaces
menacing
menagerie
menageries
mend
mended
mending
mends
menial
menials
menopause
menstrual
menstruate
menstruated
menstruates
menstruating
menstruation
mental
mentalities
mentality
mentally
menthol
mention
mentioned
mentioning
mentions
mentor
mentored
mentoring
mentors
menu
menus
meow
meowed
meowing
meows
mercantile
mercenaries
mercenary
merchandise
merchandised
merchandises
merchandising
merchandize
merchandized
merchandizes
merchandizing
merchant
merchants
mercies
merciful
mercifully
merciless
mercilessly
mercury
mercy
mere
merely
meres
merest
merge
merged
merger
mergers
merges
merging
meridian
meridians
meringue
meringues
merit
merited
meriting
merits
mermaid
mermaids
merrier
merriest
merrily
merriment
merry
mes
mesdames
mesh
meshed
meshes
meshing
mess
message
messages
messed
messenger
messengers
messes
messier
messiest
messing
messy
met
metabolic
metabolism
metabolisms
metal
metallic
metallurgy
metals
metamorphose
metamorphoses
metamorphosis
metaphor
metaphorical
metaphorically
metaphors
metaphysical
metaphysics
mete
meted
meteor
meteoric
meteorite
meteorites
meteorologist
meteorologists
meteorology
meteors
meter
metered
metering
meters
metes
method
methodical
methodology
methods
meticulous
meting
metric
metro
metropolis
metropolises
metropolitan
metros
mettle
mew
mewed
mewing
mews
mezzanine
mezzanines
miaow
miaowed
miaowing
miaows
mice
microbe
microbes
microbiology
microcode
microcomputer
microcomputers
microfiche
microfiches
microfilm
microfilmed
microfilming
microfilms
micrometer
micrometers
microorganism
microorganisms
microphone
microphones
microprocessor
microscope
microscopes
microscopic
microsecond
microseconds
microwave
microwaved
microwaves
microwaving
midday
middle
middleman
middlemen
middles
midget
midgets
midnight
midriff
midriffs
midst
midstream
midsummer
midway
midways
midwife
midwifed
midwifes
midwifing
midwived
midwives
midwiving
mien
miens
might
mightier
mightiest
mighty
migraine
migraines
migrant
migrants
migrate
migrated
migrates
migrating
migration
migrations
migratory
mike
miked
mikes
miking
mild
milder
mildest
mildew
mildewed
mildewing
mildews
mildly
mile
mileage
mileages
miles
milestone
milestones
militancy
militant
militants
militaries
militarily
military
militate
militated
militates
militating
militia
militias
milk
milked
milker
milkier
milkiest
milking
milkman
milkmen
milks
milky
mill
milled
miller
millers
milligram
milligrams
millimeter
millimeters
milliner
milliners
millinery
milling
million
millionaire
millionaires
millions
millionth
millionths
millisecond
milliseconds
mills
mime
mimed
mimes
mimic
mimicked
mimicking
mimicries
mimicry
mimics
miming
mince
minced
mincemeat
minces
mincing
mind
mindbogglingly
minded
mindedness
mindful
minding
mindless
mindlessly
minds
mine
mined
minefield
miner
mineral
minerals
miners
mines
mingle
mingled
mingles
mingling
miniature
miniatures
minibus
minibuses
minibusses
minicomputer
minima
minimal
minimalism
minimalist
minimally
minimize
minimized
minimizes
minimizing
minimum
minimums
mining
minion
minions
miniscule
miniscules
minister
ministered
ministerial
ministering
ministers
ministries
ministry
mink
minks
minnow
minnows
minor
minored
minoring
minorities
minority
minors
minstrel
minstrels
mint
minted
minting
mints
minuet
minuets
minus
minuscule
minuscules
minuses
minute
minuted
minuter
minutes
minutest
minuting
miracle
miracles
miraculous
miraculously
mirage
mirages
mire
mired
mires
miring
mirror
mirrored
mirroring
mirrors
mirth
misadventure
misadventures
misapprehension
misappropriate
misappropriated
misappropriates
misappropriating
misappropriation
misappropriations
misbehave
misbehaved
misbehaves
misbehaving
misbehavior
miscarriage
miscarriages
miscarried
miscarries
miscarry
miscarrying
miscellaneous
miscellany
mischief
mischievous
misconception
misconceptions
misconduct
misconducted
misconducting
misconducts
misconstrue
misconstrued
misconstrues
misconstruing
misdeed
misdeeds
misdemeanor
misdemeanors
misdirect
misdirected
misdirecting
misdirection
misdirects
miser
miserable
miserably
miseries
miserly
misers
misery
misfit
misfits
misfitted
misfitting
misfortune
misfortunes
misgiving
misgivings
misguide
misguided
misguides
misguiding
mishap
mishaps
misinform
misinformation
misinformed
misinforming
misinforms
misinterpret
misinterpretation
misinterpreted
misinterpreting
misinterprets
misjudge
misjudged
misjudges
misjudging
mislaid
mislay
mislaying
mislays
mislead
misleading
misleads
misled
mismanagement
mismatch
mismatched
mismatches
mismatching
misnomer
misnomers
misplace
misplaced
misplaces
misplacing
misprint
misprinted
misprinting
misprints
misquote
misquoted
misquotes
misquoting
misread
misreading
misreads
misrepresent
misrepresentation
misrepresentations
misrepresented
misrepresenting
misrepresents
miss
missed
misses
misshapen
missile
missiles
missing
mission
missionaries
missionary
missions
missive
missives
misspell
misspelled
misspelling
misspellings
misspells
misspelt
mist
mistake
mistaken
mistakenly
mistakes
mistaking
misted
mistier
mistiest
misting
mistletoe
mistook
mistress
mistresses
mistrust
mistrusted
mistrusting
mistrusts
mists
misty
mistype
mistyping
misunderstand
misunderstanding
misunderstandings
misunderstands
misunderstood
misuse
misused
misuses
misusing
mite
mites
mitigate
mitigated
mitigates
mitigating
mitt
mitten
mittens
mitts
mix
mixed
mixer
mixers
mixes
mixing
mixture
mixtures
mnemonic
mnemonics
moan
moaned
moaning
moans
moat
moats
mob
mobbed
mobbing
mobile
mobiles
mobility
mobilization
mobilizations
mobilize
mobilized
mobilizes
mobilizing
mobs
moccasin
moccasins
mock
mocked
mockeries
mockery
mocking
mockingbird
mockingbirds
mocks
mod
modal
mode
model
modeled
modeling
modelings
modelled
modelling
models
moderate
moderated
moderately
moderates
moderating
moderation
moderator
moderators
modern
modernity
modernization
modernize
modernized
modernizes
modernizing
moderns
modes
modest
modestly
modesty
modicum
modicums
modification
modifications
modified
modifier
modifiers
modifies
modify
modifying
modular
modulate
modulated
modulates
modulating
modulation
modulations
module
modules
mohair
moist
moisten
moistened
moistening
moistens
moister
moistest
moisture
molar
molars
molasses
mold
molded
moldier
moldiest
molding
moldings
molds
moldy
mole
molecular
molecule
molecules
moles
molest
molested
molesting
molests
mollified
mollifies
mollify
mollifying
mollusc
molluscs
mollusk
mollusks
molt
molted
molten
molting
molts
mom
moment
momentarily
momentary
momentous
moments
momentum
momma
mommas
moms
monarch
monarchies
monarchs
monarchy
monasteries
monastery
monastic
monastics
monetarism
monetary
money
mongoose
mongrel
mongrels
monies
monitor
monitored
monitoring
monitors
monk
monkey
monkeyed
monkeying
monkeys
monks
monochrome
monogamous
monogamy
monogram
monogrammed
monogramming
monograms
monolithic
monolog
monologs
monologue
monologues
monopolies
monopolize
monopolized
monopolizes
monopolizing
monopoly
monorail
monorails
monosyllable
monosyllables
monotonically
monotonous
monotony
monsoon
monsoons
monster
monsters
monstrosities
monstrosity
monstrous
month
monthlies
monthly
months
monument
monumental
monuments
moo
mood
moodier
moodiest
moodily
moods
moody
mooed
mooing
moon
moonbeam
moonbeams
mooned
mooning
moonlight
moonlighted
moonlighting
moonlights
moons
moor
moored
mooring
moorings
moors
moos
moose
moot
mooted
mooting
moots
mop
mope
moped
mopes
moping
mopped
mopping
mops
moral
morale
moralist
moralists
moralities
morality
morally
morals
morass
morasses
moratoria
moratorium
moratoriums
morbid
more
moreover
morgue
morgues
morn
morning
mornings
morns
moron
moronic
morons
morose
morphine
morphology
morsel
morsels
mortal
mortality
mortally
mortals
mortar
mortared
mortaring
mortars
mortgage
mortgaged
mortgages
mortgaging
mortification
mortified
mortifies
mortify
mortifying
mortuaries
mortuary
mosaic
mosaics
mosque
mosques
mosquito
mosquitoes
mosquitos
moss
mosses
mossier
mossiest
mossy
most
mostly
motel
motels
moth
mothball
mothballed
mothballing
mothballs
mother
mothered
motherhood
mothering
motherly
mothers
moths
motif
motifs
motion
motioned
motioning
motionless
motions
motivate
motivated
motivates
motivating
motivation
motivations
motive
motives
motley
motleys
motlier
motliest
motor
motorbike
motorbikes
motorcade
motorcades
motorcycle
motorcycled
motorcycles
motorcycling
motored
motoring
motorist
motorists
motorize
motorized
motorizes
motorizing
motors
motorway
motorways
motto
mottoes
mottos
mound
mounded
mounding
mounds
mount
mountain
mountaineer
mountaineered
mountaineering
mountaineers
mountainous
mountains
mounted
mounting
mounts
mourn
mourned
mourner
mourners
mournful
mourning
mourns
mouse
moused
mouses
mousey
mousier
mousiest
mousing
mousse
moussed
mousses
moussing
moustache
moustaches
mousy
mouth
mouthed
mouthful
mouthfuls
mouthing
mouthpiece
mouthpieces
mouths
movable
movables
move
moveable
moveables
moved
movement
movements
mover
movers
moves
movie
movies
moving
mow
mowed
mower
mowers
mowing
mown
mows
ms
mu
much
muck
mucked
mucking
mucks
mucous
mucus
mud
muddied
muddier
muddies
muddiest
muddle
muddled
muddles
muddling
muddy
muddying
muff
muffed
muffin
muffing
muffins
muffle
muffled
muffler
mufflers
muffles
muffling
muffs
mug
mugged
mugger
muggers
muggier
muggiest
mugginess
mugging
muggy
mugs
mulch
mulched
mulches
mulching
mule
mules
mull
mulled
mulling
mulls
multinational
multinationals
multiple
multiples
multiplication
multiplications
multiplicative
multiplicities
multiplicity
multiplied
multiplies
multiply
multiplying
multiprocessing
multitasking
multitude
multitudes
mum
mumble
mumbled
mumbles
mumbling
mummies
mummified
mummifies
mummify
mummifying
mummy
mumps
mums
munch
munched
munches
munching
mundane
municipal
municipalities
municipality
municipals
mural
murals
murder
murdered
murderer
murderers
murdering
murderous
murders
murkier
murkiest
murky
murmur
murmured
murmuring
murmurs
muscle
muscled
muscles
muscling
muscular
muse
mused
muses
museum
museums
mush
mushed
mushes
mushier
mushiest
mushing
mushroom
mushroomed
mushrooming
mushrooms
mushy
music
musical
musically
musicals
musician
musicians
musing
musk
musket
muskets
muss
mussed
mussel
mussels
musses
mussing
must
mustache
mustaches
mustang
mustangs
mustard
muster
mustered
mustering
musters
mustier
mustiest
musts
musty
mutant
mutants
mutate
mutated
mutates
mutating
mutation
mutations
mute
muted
mutely
muter
mutes
mutest
mutilate
mutilated
mutilates
mutilating
mutilation
mutilations
muting
mutinied
mutinies
mutinous
mutiny
mutinying
mutt
mutter
muttered
muttering
mutters
mutton
mutts
mutual
mutually
muzzle
muzzled
muzzles
muzzling
my
myopic
myriad
myriads
mys
myself
mysteries
mysterious
mysteriously
mystery
mystic
mystical
mysticism
mystics
mystified
mystifies
mystify
mystifying
myth
mythical
mythological
mythologies
mythology
myths
nab
nabbed
nabbing
nabs
nag
nagged
nagging
nags
nail
nailed
nailing
nails
naive
naively
naiver
naivest
naivety
naked
nakedness
name
named
nameless
namely
names
namesake
namesakes
naming
nap
napalm
napalmed
napalming
napalms
nape
napes
napkin
napkins
napped
nappies
napping
nappy
naps
narcotic
narcotics
narrate
narrated
narrates
narrating
narration
narrations
narrative
narratives
narrator
narrators
narrow
narrowed
narrower
narrowest
narrowing
narrowly
narrowness
narrows
nasal
nasals
nastier
nastiest
nastily
nastiness
nasty
nation
national
nationalism
nationalist
nationalistic
nationalists
nationalities
nationality
nationalize
nationalized
nationalizes
nationalizing
nationally
nationals
nations
nationwide
native
natives
nativities
nativity
nattier
nattiest
natty
natural
naturalist
naturalists
naturalization
naturalize
naturalized
naturalizes
naturalizing
naturally
naturalness
naturals
nature
natures
naught
naughtier
naughtiest
naughtily
naughtiness
naughts
naughty
nausea
nauseate
nauseated
nauseates
nauseating
nauseous
nautical
naval
navel
navels
navies
navigable
navigate
navigated
navigates
navigating
navigation
navigator
navigators
navy
nay
nays
near
nearby
neared
nearer
nearest
nearing
nearly
nears
nearsighted
nearsightedness
neat
neater
neatest
neatly
neatness
nebula
nebulae
nebulas
nebulous
necessaries
necessarily
necessary
necessitate
necessitated
necessitates
necessitating
necessities
necessity
neck
necked
neckerchief
neckerchiefs
neckerchieves
necking
necklace
necklaces
neckline
necklines
necks
necktie
neckties
necrophilia
nectar
nectarine
nectarines
need
needed
needier
neediest
needing
needle
needled
needles
needless
needlessly
needlework
needling
needs
needy
negate
negated
negates
negating
negation
negations
negative
negatived
negatively
negatives
negativing
neglect
neglected
neglectful
neglecting
neglects
neglig
negligee
negligees
negligence
negligent
negligently
negligible
negligs
negotiable
negotiate
negotiated
negotiates
negotiating
negotiation
negotiations
negotiator
negotiators
neigh
neighbor
neighbored
neighborhood
neighborhoods
neighboring
neighborliness
neighborly
neighbors
neighed
neighing
neighs
neither
neon
neophyte
neophytes
nephew
nephews
nepotism
nerve
nerved
nerves
nerving
nervous
nervously
nervousness
nest
nested
nesting
nestle
nestled
nestles
nestling
nests
net
nether
nets
netted
netting
nettle
nettled
nettles
nettling
network
networked
networking
networks
neural
neurologist
neurologists
neurology
neuron
neurons
neuroses
neurosis
neurotic
neurotics
neuter
neutered
neutering
neuters
neutral
neutrality
neutralize
neutralized
neutralizes
neutralizing
neutrals
neutron
neutrons
never
nevertheless
new
newbie
newbies
newborn
newborns
newcomer
newcomers
newer
newest
newfangled
newly
news
newsagents
newscast
newscaster
newscasters
newscasts
newsier
newsiest
newsletter
newsletters
newspaper
newspapers
newsprint
newsstand
newsstands
newsy
newt
newton
newts
next
nibble
nibbled
nibbles
nibbling
nice
nicely
nicer
nicest
niceties
nicety
niche
niches
nick
nicked
nickel
nickels
nicking
nickname
nicknamed
nicknames
nicknaming
nicks
nicotine
niece
nieces
niftier
niftiest
nifty
nigh
night
nightclub
nightclubbed
nightclubbing
nightclubs
nightfall
nightgown
nightgowns
nightingale
nightingales
nightly
nightmare
nightmares
nightmarish
nights
nighttime
nil
nimble
nimbler
nimblest
nimbly
nincompoop
nincompoops
nine
nines
nineteen
nineteens
nineteenth
nineteenths
nineties
ninetieth
ninetieths
ninety
ninnies
ninny
ninth
ninths
nip
nipped
nippier
nippiest
nipping
nipple
nipples
nippy
nips
nit
nite
nites
nitrate
nitrated
nitrates
nitrating
nitrogen
nits
nitwit
nitwits
no
nobility
noble
nobleman
noblemen
nobler
nobles
noblest
noblewoman
noblewomen
nobly
nobodies
nobody
nocturnal
nod
nodded
nodding
node
nodes
nods
noes
noise
noised
noiseless
noiselessly
noises
noisier
noisiest
noisily
noisiness
noising
noisy
nomad
nomadic
nomads
nomenclature
nomenclatures
nominal
nominally
nominate
nominated
nominates
nominating
nomination
nominations
nominative
nominatives
nominee
nominees
non
nonchalance
nonchalant
nonchalantly
noncommittal
nonconformist
nonconformists
nondescript
none
nonentities
nonentity
nonetheless
nonfiction
nonflammable
nonpartisan
nonpartisans
nonprofit
nonprofits
nonresident
nonresidents
nonsense
nonsensical
nonstandard
nonstop
nontrivial
nonviolence
noodle
noodled
noodles
noodling
nook
nooks
noon
noose
nooses
nor
norm
normal
normality
normally
norms
north
northeast
northeasterly
northeastern
northerlies
northerly
northern
northward
northwest
northwestern
nose
nosebleed
nosebleeds
nosed
noses
nosey
nosier
nosiest
nosing
nostalgia
nostalgic
nostril
nostrils
nosy
not
notable
notables
notably
notation
notations
notch
notched
notches
notching
note
notebook
notebooks
noted
notes
noteworthy
nothing
nothingness
nothings
notice
noticeable
noticeably
noticeboard
noticeboards
noticed
notices
noticing
notification
notifications
notified
notifies
notify
notifying
noting
notion
notional
notions
notoriety
notorious
notoriously
notwithstanding
nougat
nougats
nought
noughts
noun
nouns
nourish
nourished
nourishes
nourishing
nourishment
nova
novel
novelist
novelists
novels
novelties
novelty
novice
novices
now
nowadays
nowhere
noxious
nozzle
nozzles
nuance
nuances
nuclear
nuclei
nucleus
nucleuses
nude
nuder
nudes
nudest
nudge
nudged
nudges
nudging
nudity
nugget
nuggets
nuisance
nuisances
null
nullified
nullifies
nullify
nullifying
nulls
numb
numbed
number
numbered
numbering
numbers
numbest
numbing
numbness
numbs
numeral
numerals
numerate
numerator
numerators
numeric
numerical
numerically
numerous
nun
nuns
nuptial
nuptials
nurse
nursed
nursemaid
nursemaids
nurseries
nursery
nurses
nursing
nurture
nurtured
nurtures
nurturing
nut
nutcracker
nutcrackers
nutmeg
nutmegs
nutrient
nutrients
nutriment
nutriments
nutrition
nutritional
nutritious
nuts
nutshell
nutshells
nutted
nuttier
nuttiest
nutting
nutty
nuzzle
nuzzled
nuzzles
nuzzling
nylon
nymph
nymphs
oaf
oafs
oak
oaks
oar
oared
oaring
oars
oases
oasis
oath
oaths
oatmeal
obedience
obedient
obediently
obelisk
obelisks
obese
obesity
obey
obeyed
obeying
obeys
obfuscation
obituaries
obituary
object
objected
objecting
objection
objectionable
objections
objective
objectively
objectives
objectivity
objector
objectors
objects
obligate
obligated
obligates
obligating
obligation
obligations
obligatory
oblige
obliged
obliges
obliging
oblique
obliques
obliterate
obliterated
obliterates
obliterating
obliteration
oblivion
oblivious
oblong
oblongs
obnoxious
oboe
oboes
obscene
obscener
obscenest
obscenities
obscenity
obscure
obscured
obscurer
obscures
obscurest
obscuring
obscurities
obscurity
observable
observance
observances
observant
observation
observations
observatories
observatory
observe
observed
observer
observers
observes
observing
obsess
obsessed
obsesses
obsessing
obsession
obsessions
obsessive
obsolescence
obsolescent
obsolete
obsoleted
obsoletes
obsoleting
obstacle
obstacles
obstetrician
obstetricians
obstetrics
obstinacy
obstinate
obstruct
obstructed
obstructing
obstruction
obstructions
obstructive
obstructs
obtain
obtainable
obtained
obtaining
obtains
obtrusive
obtuse
obtuser
obtusest
obvious
obviously
occasion
occasional
occasionally
occasioned
occasioning
occasions
occupancy
occupant
occupants
occupation
occupational
occupations
occupied
occupies
occupy
occupying
occur
occurred
occurrence
occurrences
occurring
occurs
ocean
oceanic
oceanography
oceans
octagon
octagonal
octagons
octal
octave
octaves
octopi
octopus
octopuses
ocular
oculars
odd
odder
oddest
oddities
oddity
oddly
odds
ode
odes
odious
odometer
odometers
odor
odors
of
off
offbeat
offbeats
offed
offend
offended
offender
offenders
offending
offends
offense
offenses
offensive
offensiveness
offensives
offer
offered
offering
offerings
offers
offhand
office
officer
officers
offices
official
officially
officials
officiate
officiated
officiates
officiating
officious
offing
offings
offload
offs
offset
offsets
offsetting
offshoot
offshoots
offshore
offspring
offsprings
offstage
offstages
often
oftener
oftenest
ogle
ogled
ogles
ogling
ogre
ogres
oh
ohm
ohms
ohs
oil
oiled
oilier
oiliest
oiling
oils
oily
ointment
ointments
okay
okayed
okaying
okays
okra
okras
old
olden
older
oldest
olfactories
olfactory
olive
olives
omega
omelet
omelets
omelette
omelettes
omen
omens
ominous
ominously
omission
omissions
omit
omits
omitted
omitting
omnibus
omnipotence
omnipotent
omnipresent
omniscient
on
once
oncoming
one
onerous
ones
oneself
ongoing
onion
onions
onlooker
onlookers
only
onomatopoeia
onrush
onrushes
onset
onsets
onslaught
onslaughts
onto
onus
onuses
onward
onwards
oodles
ooze
oozed
oozes
oozing
opal
opals
opaque
opaqued
opaquer
opaques
opaquest
opaquing
open
opened
opener
openers
openest
opening
openings
openly
openness
opens
opera
operand
operands
operas
operate
operated
operates
operatic
operating
operation
operational
operations
operative
operatives
operator
operators
ophthalmologist
ophthalmologists
ophthalmology
opinion
opinionated
opinions
opium
opossum
opossums
opponent
opponents
opportune
opportunist
opportunists
opportunities
opportunity
oppose
opposed
opposes
opposing
opposite
opposites
opposition
oppress
oppressed
oppresses
oppressing
oppression
oppressive
oppressor
oppressors
opt
opted
optic
optical
optician
opticians
optics
optima
optimal
optimism
optimist
optimistic
optimists
optimization
optimize
optimized
optimizes
optimizing
optimum
optimums
opting
option
optional
optionally
optioned
optioning
options
optometrist
optometrists
opts
opulent
opus
opuses
or
oracle
oracles
oral
orals
orange
oranges
orangutan
orangutang
orangutangs
orangutans
oration
orations
orator
oratories
orators
oratory
orbit
orbital
orbitals
orbited
orbiting
orbits
orchard
orchards
orchestra
orchestral
orchestras
orchestrate
orchestrated
orchestrates
orchestrating
orchestration
orchestrations
orchid
orchids
ordain
ordained
ordaining
ordains
ordeal
ordeals
order
ordered
ordering
orderlies
orderly
orders
ordinance
ordinances
ordinaries
ordinarily
ordinary
ordination
ordinations
ore
ores
organ
organic
organics
organism
organisms
organist
organists
organization
organizational
organizations
organize
organized
organizer
organizers
organizes
organizing
organs
orgasm
orgies
orgy
orient
oriental
orientate
orientated
orientates
orientating
orientation
orientations
oriented
orienting
orients
orifice
origin
original
originality
originally
originals
originate
originated
originates
originating
originator
originators
origins
ornament
ornamental
ornamented
ornamenting
ornaments
ornate
ornately
ornithologist
ornithologists
ornithology
orphan
orphanage
orphanages
orphaned
orphaning
orphans
orthodontist
orthodontists
orthodox
orthogonal
orthogonality
orthography
orthopaedics
orthopedics
oscillate
oscillated
oscillates
oscillating
oscillation
oscillations
oscilloscope
osmosis
ostensible
ostensibly
ostentation
ostentatious
ostracize
ostracized
ostracizes
ostracizing
ostrich
ostriches
other
others
otherwise
otter
otters
ouch
ought
ounce
ounces
our
ours
ourselves
oust
ousted
ouster
ousters
ousting
ousts
out
outbound
outbreak
outbreaks
outburst
outbursts
outcast
outcasts
outclass
outclassed
outclasses
outclassing
outcome
outcomes
outcries
outcry
outdated
outdid
outdistance
outdistanced
outdistances
outdistancing
outdo
outdoes
outdoing
outdone
outdoor
outdoors
outed
outer
outermost
outfield
outfields
outfit
outfits
outfitted
outfitting
outgoing
outgrew
outgrow
outgrowing
outgrown
outgrows
outgrowth
outgrowths
outhouse
outhouses
outing
outings
outlaid
outlandish
outlast
outlasted
outlasting
outlasts
outlaw
outlawed
outlawing
outlaws
outlay
outlaying
outlays
outlet
outlets
outline
outlined
outlines
outlining
outlive
outlived
outlives
outliving
outlook
outlooks
outlying
outmoded
outnumber
outnumbered
outnumbering
outnumbers
outpatient
outpatients
outpost
outposts
output
outputs
outputted
outputting
outrage
outraged
outrageous
outrageously
outrages
outraging
outran
outright
outrun
outrunning
outruns
outs
outset
outsets
outshine
outshined
outshines
outshining
outshone
outside
outsider
outsiders
outsides
outskirt
outskirts
outsmart
outsmarted
outsmarting
outsmarts
outspoken
outstanding
outstandingly
outstation
outstations
outstrip
outstripped
outstripping
outstrips
outstript
outward
outwardly
outwards
outweigh
outweighed
outweighing
outweighs
outwit
outwits
outwitted
outwitting
ova
oval
ovals
ovaries
ovary
ovation
ovations
oven
ovens
over
overall
overalls
overate
overbear
overbearing
overbears
overblown
overboard
overbore
overborne
overburden
overburdened
overburdening
overburdens
overcame
overcast
overcasting
overcasts
overcharge
overcharged
overcharges
overcharging
overcoat
overcoats
overcome
overcomes
overcoming
overcrowd
overcrowded
overcrowding
overcrowds
overdid
overdo
overdoes
overdoing
overdone
overdose
overdosed
overdoses
overdosing
overdraft
overdraw
overdrawing
overdrawn
overdraws
overdrew
overdue
overeat
overeaten
overeating
overeats
overestimate
overestimated
overestimates
overestimating
overflow
overflowed
overflowing
overflows
overgrew
overgrow
overgrowing
overgrown
overgrows
overhand
overhands
overhang
overhanging
overhangs
overhaul
overhauled
overhauling
overhauls
overhead
overheads
overhear
overheard
overhearing
overhears
overheat
overheated
overheating
overheats
overhung
overkill
overlaid
overlain
overland
overlap
overlapped
overlapping
overlaps
overlay
overlaying
overlays
overlie
overlies
overload
overloaded
overloading
overloads
overlong
overlook
overlooked
overlooking
overlooks
overly
overlying
overnight
overnights
overpass
overpasses
overpopulation
overpower
overpowered
overpowering
overpowers
overprice
overpriced
overprices
overpricing
overprint
overprinted
overprinting
overprints
overran
overrate
overrated
overrates
overrating
overreact
overreacted
overreacting
overreacts
overridden
override
overrides
overriding
overrode
overrule
overruled
overrules
overruling
overrun
overrunning
overruns
overs
oversampling
oversaw
overseas
oversee
overseeing
overseen
overseer
overseers
oversees
overshadow
overshadowed
overshadowing
overshadows
overshoot
overshooting
overshoots
overshot
oversight
oversights
oversimplification
oversleep
oversleeping
oversleeps
overslept
overstate
overstated
overstates
overstating
overstep
overstepped
overstepping
oversteps
overt
overtake
overtaken
overtakes
overtaking
overthrew
overthrow
overthrowing
overthrown
overthrows
overtime
overtimes
overtly
overtone
overtones
overtook
overture
overtures
overturn
overturned
overturning
overturns
overuse
overused
overuses
overusing
overview
overweight
overwhelm
overwhelmed
overwhelming
overwhelmingly
overwhelms
overwork
overworked
overworking
overworks
overwrite
overwrites
overwriting
overwritten
overwrought
ovum
owe
owed
owes
owing
owl
owls
own
owned
owner
owners
ownership
owning
owns
ox
oxen
oxidation
oxide
oxides
oxidize
oxidized
oxidizes
oxidizing
oxygen
oyster
oysters
ozone
pa
pace
paced
pacemaker
pacemakers
paces
pacific
pacified
pacifier
pacifiers
pacifies
pacifism
pacifist
pacifists
pacify
pacifying
pacing
pack
package
packaged
packages
packaging
packed
packer
packers
packet
packets
packing
packs
pact
pacts
pad
padded
paddies
padding
paddle
paddled
paddles
paddling
paddock
paddocked
paddocking
paddocks
paddy
padlock
padlocked
padlocking
padlocks
pads
pagan
pagans
page
pageant
pageantry
pageants
paged
pager
pages
pagination
paging
pagoda
pagodas
paid
pail
pails
pain
pained
painful
painfuller
painfullest
painfully
paining
painless
painlessly
pains
painstaking
paint
painted
painter
painting
paintings
paints
pair
paired
pairing
pairs
pajamas
pal
palace
palaces
palatable
palate
palates
palatial
pale
paled
paleontologist
paleontologists
paleontology
paler
pales
palest
palette
palettes
paling
pall
pallbearer
pallbearers
palled
pallid
palling
pallor
palls
palm
palmed
palming
palms
palomino
palominos
palpable
palpably
pals
paltrier
paltriest
paltry
pamper
pampered
pampering
pampers
pamphlet
pamphlets
pan
panacea
panaceas
pancake
pancaked
pancakes
pancaking
pancreas
pancreases
pancreatic
panda
pandas
pandemonium
pander
pandered
pandering
panders
pane
panel
paneled
paneling
panelled
panelling
panellings
panels
panes
pang
pangs
panhandle
panhandled
panhandler
panhandlers
panhandles
panhandling
panic
panicked
panickier
panickiest
panicking
panicky
panics
panned
panning
panorama
panoramas
panoramic
pans
pansies
pansy
pant
panted
panther
panthers
pantie
panties
panting
pantomime
pantomimed
pantomimes
pantomiming
pantries
pantry
pants
panty
pap
papa
papacies
papacy
papal
papas
papaya
papayas
paper
paperback
paperbacks
papered
papering
papers
paperweight
paperweights
paperwork
paprika
papyri
papyrus
papyruses
par
parable
parables
parachute
parachuted
parachutes
parachuting
parade
paraded
parades
paradigm
parading
paradise
paradises
paradox
paradoxes
paradoxical
paradoxically
paraffin
paragon
paragons
paragraph
paragraphed
paragraphing
paragraphs
parakeet
parakeets
parallel
paralleled
paralleling
parallelled
parallelling
parallels
paralyses
paralysis
paralytic
paralytics
paralyze
paralyzed
paralyzes
paralyzing
parameter
parameters
paramount
paranoia
paranoid
paranoids
paraphernalia
paraphrase
paraphrased
paraphrases
paraphrasing
paraplegic
paraplegics
parasite
parasites
parasitic
parasol
parasols
paratrooper
paratroopers
parcel
parceled
parceling
parcelled
parcelling
parcels
parch
parched
parches
parching
parchment
parchments
pardon
pardonable
pardoned
pardoning
pardons
pare
pared
parent
parentage
parental
parented
parentheses
parenthesis
parenthetical
parenthood
parenting
parents
pares
paring
parish
parishes
parishioner
parishioners
parity
park
parka
parkas
parked
parking
parks
parkway
parkways
parliament
parliamentary
parliaments
parlor
parlors
parochial
parodied
parodies
parody
parodying
parole
paroled
paroles
paroling
parrakeet
parrakeets
parred
parring
parrot
parroted
parroting
parrots
pars
parse
parsec
parsecs
parsed
parser
parses
parsing
parsley
parsnip
parsnips
parson
parsonage
parsonages
parsons
part
partake
partaken
partakes
partaking
parted
partial
partiality
partially
partials
participant
participants
participate
participated
participates
participating
participation
participle
participles
particle
particles
particular
particularly
particulars
partied
parties
parting
partings
partisan
partisans
partition
partitioned
partitioning
partitions
partizan
partizans
partly
partner
partnered
partnering
partners
partnership
partnerships
partook
partridge
partridges
parts
party
partying
pas
pass
passable
passage
passages
passageway
passageways
passbook
passbooks
passed
passenger
passengers
passer
passes
passing
passion
passionate
passionately
passions
passive
passively
passives
passport
passports
password
passwords
past
pasta
pastas
paste
pasted
pastel
pastels
pastes
pasteurization
pasteurize
pasteurized
pasteurizes
pasteurizing
pastiche
pastier
pasties
pastiest
pastime
pastimes
pasting
pastor
pastoral
pastorals
pastors
pastries
pastry
pasts
pasture
pastured
pastures
pasturing
pasty
pat
patch
patched
patches
patching
patchwork
patchworks
patchy
pate
patent
patented
patenting
patently
patents
paternal
paternalism
paternity
pates
path
pathetic
pathetically
pathological
pathologist
pathologists
pathology
pathos
paths
pathway
pathways
patience
patient
patienter
patientest
patiently
patients
patio
patios
patriarch
patriarchal
patriarchs
patrimonies
patrimony
patriot
patriotic
patriotism
patriots
patrol
patrolled
patrolling
patrols
patron
patronage
patronages
patronize
patronized
patronizes
patronizing
patrons
pats
patted
patter
pattered
pattering
pattern
patterned
patterning
patterns
patters
patties
patting
patty
paucity
paunch
paunches
paunchier
paunchiest
paunchy
pauper
paupers
pause
paused
pauses
pausing
pave
paved
pavement
pavements
paves
pavilion
pavilions
paving
paw
pawed
pawing
pawn
pawnbroker
pawnbrokers
pawned
pawning
pawns
paws
pay
payable
payed
payer
payers
paying
payload
payment
payments
payoff
payoffs
payroll
payrolls
pays
pea
peace
peaceable
peaceful
peacefully
peacemaker
peacemakers
peaces
peach
peaches
peacock
peacocks
peak
peaked
peaking
peaks
peal
pealed
pealing
peals
peanut
peanuts
pear
pearl
pearled
pearling
pearls
pears
peas
peasant
peasants
pease
peat
pebble
pebbled
pebbles
pebbling
pecan
pecans
peck
pecked
pecking
pecks
peculiar
peculiarities
peculiarity
peculiarly
pedagogy
pedal
pedaled
pedaling
pedalled
pedalling
pedals
pedant
pedantic
pedantry
pedants
peddle
peddled
peddler
peddlers
peddles
peddling
pedestal
pedestals
pedestrian
pedestrians
pediatrician
pediatricians
pediatrics
pediatrist
pediatrists
pedigree
pedigrees
pedlar
pedlars
peek
peeked
peeking
peeks
peel
peeled
peeling
peels
peep
peeped
peeping
peeps
peer
peered
peering
peerless
peers
peeve
peeved
peeves
peeving
peevish
peg
pegged
pegging
pegs
pelican
pelicans
pellet
pelleted
pelleting
pellets
pelt
pelted
pelting
pelts
pelves
pelvic
pelvis
pelvises
pen
penal
penalize
penalized
penalizes
penalizing
penalties
penalty
penance
penances
pence
penchant
pencil
penciled
penciling
pencilled
pencilling
pencils
pendant
pendants
pended
pending
pends
pendulum
pendulums
penes
penetrate
penetrated
penetrates
penetrating
penetration
penetrations
penguin
penguins
penicillin
peninsula
peninsulas
penis
penises
penitence
penitent
penitentiaries
penitentiary
penitents
penknife
penknives
penmanship
pennant
pennants
penned
pennies
penniless
penning
penny
pens
pension
pensioned
pensioner
pensioners
pensioning
pensions
pensive
pensively
pentagon
pentagonal
pentagons
penthouse
penthouses
penultimate
peon
peonies
peons
peony
people
peopled
peoples
peopling
pep
pepped
pepper
peppered
peppering
peppermint
peppermints
peppers
pepping
peps
per
perceive
perceived
perceives
perceiving
percent
percentage
percentages
percents
perceptible
perception
perceptions
perceptive
perch
perchance
perched
perches
perching
percolate
percolated
percolates
percolating
percolation
percolator
percolators
percussion
peremptory
perennial
perennials
perfect
perfected
perfecter
perfectest
perfecting
perfection
perfectionist
perfectionists
perfections
perfectly
perfects
perforate
perforated
perforates
perforating
perforation
perforations
perform
performance
performances
performed
performer
performers
performing
performs
perfume
perfumed
perfumes
perfuming
perfunctorily
perfunctory
perhaps
peril
periled
periling
perilled
perilling
perilous
perilously
perils
perimeter
perimeters
period
periodic
periodical
periodically
periodicals
periods
peripheral
peripherals
peripheries
periphery
periscope
periscopes
perish
perishable
perishables
perished
perishes
perishing
perjure
perjured
perjures
perjuries
perjuring
perjury
perk
perked
perkier
perkiest
perking
perks
perky
permanence
permanent
permanently
permanents
permeate
permeated
permeates
permeating
permissible
permission
permissions
permissive
permit
permits
permitted
permitting
permutation
permutations
pernicious
peroxide
peroxided
peroxides
peroxiding
perpendicular
perpendiculars
perpetrate
perpetrated
perpetrates
perpetrating
perpetrator
perpetrators
perpetual
perpetually
perpetuals
perpetuate
perpetuated
perpetuates
perpetuating
perplex
perplexed
perplexes
perplexing
perplexities
perplexity
persecute
persecuted
persecutes
persecuting
persecution
persecutions
persecutor
persecutors
perseverance
persevere
persevered
perseveres
persevering
persist
persisted
persistence
persistent
persistently
persisting
persists
person
persona
personable
personal
personalities
personality
personalize
personalized
personalizes
personalizing
personally
personals
personification
personifications
personified
personifies
personify
personifying
personnel
persons
perspective
perspectives
perspiration
perspire
perspired
perspires
perspiring
persuade
persuaded
persuades
persuading
persuasion
persuasions
persuasive
persuasively
pert
pertain
pertained
pertaining
pertains
perter
pertest
pertinent
perturb
perturbed
perturbing
perturbs
perusal
perusals
peruse
perused
peruses
perusing
pervade
pervaded
pervades
pervading
pervasive
perverse
perversion
perversions
pervert
perverted
perverting
perverts
peskier
peskiest
pesky
pessimism
pessimist
pessimistic
pessimists
pest
pester
pestered
pestering
pesters
pesticide
pesticides
pestilence
pestilences
pests
pet
petal
petals
peter
petered
petering
peters
petite
petites
petition
petitioned
petitioning
petitions
petrified
petrifies
petrify
petrifying
petrol
petroleum
pets
petted
petticoat
petticoats
pettier
pettiest
pettiness
petting
petty
petulant
petunia
petunias
pew
pews
pewter
pewters
phantasied
phantasies
phantasy
phantasying
phantom
phantoms
pharmaceutical
pharmaceuticals
pharmacies
pharmacist
pharmacists
pharmacy
phase
phased
phases
phasing
pheasant
pheasants
phenomena
phenomenal
phenomenally
phenomenon
phenomenons
philanthropic
philanthropies
philanthropist
philanthropists
philanthropy
philosopher
philosophers
philosophical
philosophies
philosophize
philosophized
philosophizes
philosophizing
philosophy
phlegm
phlegmatic
phobia
phobias
phoenix
phone
phoned
phones
phonetic
phonetics
phoney
phoneys
phonics
phonied
phonier
phonies
phoniest
phoning
phonograph
phonographs
phony
phonying
phosphor
phosphorescence
phosphorescent
phosphorus
photo
photocopied
photocopier
photocopiers
photocopies
photocopy
photocopying
photoed
photogenic
photograph
photographed
photographer
photographers
photographic
photographing
photographs
photography
photoing
photon
photons
photos
photosynthesis
phototypesetter
phrase
phrased
phraseology
phrases
phrasing
physic
physical
physically
physicals
physician
physicians
physicist
physicists
physics
physiological
physiology
physique
physiques
pi
pianist
pianists
piano
pianos
piccolo
piccolos
pick
pickaback
pickabacked
pickabacking
pickabacks
pickax
pickaxe
pickaxed
pickaxes
pickaxing
picked
picket
picketed
picketing
pickets
pickier
pickiest
picking
pickle
pickled
pickles
pickling
pickpocket
pickpockets
picks
pickup
pickups
picky
picnic
picnicked
picnicking
picnics
pictorial
pictorials
picture
pictured
pictures
picturesque
picturing
piddle
piddled
piddles
piddling
pie
piece
pieced
piecemeal
pieces
piecework
piecing
pier
pierce
pierced
pierces
piercing
piers
pies
piety
pig
pigeon
pigeonhole
pigeonholed
pigeonholes
pigeonholing
pigeons
pigged
pigging
piggish
piggyback
piggybacked
piggybacking
piggybacks
pigheaded
pigment
pigments
pigpen
pigpens
pigs
pigtail
pigtails
pike
piked
pikes
piking
pile
piled
piles
pilfer
pilfered
pilfering
pilfers
pilgrim
pilgrimage
pilgrimages
pilgrims
piling
pill
pillage
pillaged
pillages
pillaging
pillar
pillars
pilled
pilling
pillow
pillowcase
pillowcases
pillowed
pillowing
pillows
pills
pilot
piloted
piloting
pilots
pimple
pimples
pimplier
pimpliest
pimply
pin
pinch
pinched
pinches
pinching
pincushion
pincushions
pine
pineapple
pineapples
pined
pines
pining
pinion
pinioned
pinioning
pinions
pink
pinked
pinker
pinkest
pinking
pinks
pinnacle
pinnacles
pinned
pinning
pinpoint
pinpointed
pinpointing
pinpoints
pins
pint
pints
pioneer
pioneered
pioneering
pioneers
pious
pipe
piped
pipeline
pipelines
pipes
piping
pique
piqued
piques
piquing
piracy
piranha
piranhas
pirate
pirated
pirates
pirating
pirouette
pirouetted
pirouettes
pirouetting
pis
pistachio
pistachios
pistol
pistols
piston
pistons
pit
pitch
pitched
pitcher
pitchers
pitches
pitchfork
pitchforked
pitchforking
pitchforks
pitching
piteous
piteously
pitfall
pitfalls
pithier
pithiest
pithy
pitied
pities
pitiful
pitifully
pitiless
pits
pittance
pittances
pitted
pitting
pity
pitying
pivot
pivotal
pivoted
pivoting
pivots
pixie
pixies
pixy
pizza
pizzas
placard
placarded
placarding
placards
placate
placated
placates
placating
place
placed
placement
placenta
placentae
placentas
places
placid
placidly
placing
plagiarism
plagiarisms
plagiarist
plagiarists
plagiarize
plagiarized
plagiarizes
plagiarizing
plague
plagued
plagues
plaguing
plaice
plaid
plaids
plain
plainer
plainest
plainly
plains
plaintiff
plaintiffs
plaintive
plan
planar
plane
planed
planes
planet
planetaria
planetarium
planetariums
planetary
planets
planing
plank
planked
planking
planks
plankton
planned
planner
planners
planning
plans
plant
plantain
plantains
plantation
plantations
planted
planter
planters
planting
plants
plaque
plaques
plasma
plaster
plastered
plastering
plasters
plastic
plastics
plate
plateau
plateaued
plateauing
plateaus
plateaux
plated
plates
platform
platformed
platforming
platforms
plating
platinum
platitude
platitudes
platoon
platooned
platooning
platoons
platter
platters
plausibility
plausible
plausibly
play
playable
playback
played
player
players
playful
playfully
playfulness
playground
playgrounds
playhouse
playhouses
playing
playmate
playmates
playpen
playpens
plays
plaything
playthings
playwright
playwrights
plaza
plazas
plea
plead
pleaded
pleading
pleads
pleas
pleasant
pleasanter
pleasantest
pleasantly
pleasantries
pleasantry
please
pleased
pleases
pleasing
pleasings
pleasurable
pleasure
pleasured
pleasures
pleasuring
pleat
pleated
pleating
pleats
pled
pledge
pledged
pledges
pledging
plentiful
plentifully
plenty
plethora
pliable
pliant
plied
pliers
plies
plight
plighted
plighting
plights
plod
plodded
plodding
plods
plop
plopped
plopping
plops
plot
plots
plotted
plotter
plotters
plotting
plough
ploughed
ploughing
ploughs
plow
plowed
plowing
plows
ploy
ploys
pluck
plucked
plucking
plucks
plucky
plug
plugged
plugging
plugs
plum
plumage
plumb
plumbed
plumber
plumbers
plumbing
plumbs
plume
plumed
plumes
pluming
plummer
plummest
plummet
plummeted
plummeting
plummets
plump
plumped
plumper
plumpest
plumping
plumps
plums
plunder
plundered
plundering
plunders
plunge
plunged
plunger
plungers
plunges
plunging
plural
plurality
plurals
plus
pluses
plush
plusher
plushest
plusses
plutonium
ply
plying
plywood
pneumatic
pneumonia
poach
poached
poacher
poachers
poaches
poaching
pocket
pocketbook
pocketbooks
pocketed
pocketing
pockets
pockmark
pockmarked
pockmarking
pockmarks
pod
podded
podding
podia
podium
podiums
pods
poem
poems
poet
poetic
poetical
poetry
poets
poignancy
poignant
poinsettia
poinsettias
point
pointed
pointedly
pointer
pointers
pointing
pointless
pointlessly
points
poise
poised
poises
poising
poison
poisoned
poisoning
poisonous
poisons
poke
poked
poker
pokers
pokes
pokey
pokier
pokiest
poking
poky
polar
polarity
polarization
polarize
polarized
polarizes
polarizing
pole
poled
polemic
polemics
poles
police
policed
policeman
policemen
polices
policewoman
policewomen
policies
policing
policy
poling
polio
polios
polish
polished
polishes
polishing
polite
politely
politeness
politer
politest
political
politically
politician
politicians
politics
polka
polkaed
polkaing
polkas
poll
polled
pollen
pollinate
pollinated
pollinates
pollinating
pollination
polling
polls
pollster
pollsters
pollutant
pollutants
pollute
polluted
pollutes
polluting
pollution
polo
polygamous
polygamy
polygon
polygons
polynomial
polynomials
polyp
polyps
polytechnic
pomegranate
pomegranates
pomp
pompous
poncho
ponchos
pond
ponder
pondered
pondering
ponderous
ponders
ponds
ponies
pontoon
pontoons
pony
poodle
poodles
pool
pooled
pooling
pools
poop
pooped
pooping
poops
poor
poorer
poorest
poorly
pop
popcorn
pope
poplar
poplars
popped
poppies
popping
poppy
pops
populace
populaces
popular
popularity
popularize
popularized
popularizes
popularizing
popularly
populate
populated
populates
populating
population
populations
populous
porcelain
porch
porches
porcupine
porcupines
pore
pored
pores
poring
pork
pornographic
pornography
porous
porpoise
porpoised
porpoises
porpoising
porridge
port
portability
portable
portables
portal
portals
ported
portend
portended
portending
portends
portent
portents
porter
porters
portfolio
portfolios
porthole
portholes
portico
porticoes
porticos
porting
portion
portioned
portioning
portions
portlier
portliest
portly
portrait
portraits
portray
portrayal
portrayals
portrayed
portraying
portrays
ports
pose
posed
poses
posies
posing
position
positional
positioned
positioning
positions
positive
positively
positives
positivism
possess
possessed
possesses
possessing
possession
possessions
possessive
possessives
possessor
possessors
possibilities
possibility
possible
possibles
possibly
possum
possums
post
postage
postal
postbox
postcard
postcards
postcode
posted
poster
posterior
posteriors
posterity
posters
postgraduate
postgraduates
posthumous
posthumously
posting
postman
postmark
postmarked
postmarking
postmarks
postmaster
postmasters
postmen
postpone
postponed
postponement
postponements
postpones
postponing
posts
postscript
postscripts
postulate
postulated
postulates
postulating
posture
postured
postures
posturing
posy
pot
potassium
potato
potatoes
potency
potent
potential
potentially
pothole
potholes
potion
potions
pots
potted
potter
pottered
potteries
pottering
potters
pottery
potting
pouch
pouched
pouches
pouching
poultry
pounce
pounced
pounces
pouncing
pound
pounded
pounding
pounds
pour
poured
pouring
pours
pout
pouted
pouting
pouts
poverty
powder
powdered
powdering
powders
powdery
power
powered
powerful
powerfully
powerhouse
powerhouses
powering
powerless
powers
powwow
powwowed
powwowing
powwows
practicable
practical
practicalities
practicality
practically
practicals
practice
practiced
practices
practicing
practise
practised
practises
practising
practitioner
practitioners
pragmatic
pragmatics
pragmatism
prairie
prairies
praise
praised
praises
praiseworthy
praising
pram
prance
pranced
prances
prancing
prank
pranks
prattle
prattled
prattles
prattling
prawn
prawned
prawning
prawns
pray
prayed
prayer
prayers
praying
prays
preach
preached
preacher
preachers
preaches
preaching
preamble
preambled
preambles
preambling
precarious
precariously
precaution
precautionary
precautions
precede
preceded
precedence
precedent
precedents
precedes
preceding
precinct
precincts
precious
precipice
precipices
precipitate
precipitated
precipitates
precipitating
precipitation
precipitations
precipitous
precise
precisely
preciser
precisest
precision
preclude
precluded
precludes
precluding
precocious
preconceive
preconceived
preconceives
preconceiving
preconception
preconceptions
precursor
precursors
predator
predators
predatory
predecessor
predecessors
predefined
predestination
predicament
predicaments
predicate
predicated
predicates
predicating
predict
predictable
predictably
predicted
predicting
prediction
predictions
predictor
predicts
predisposition
predispositions
predominance
predominant
predominantly
predominate
predominated
predominates
predominating
preeminence
preeminent
preempt
preempted
preempting
preempts
preen
preened
preening
preens
prefab
prefabbed
prefabbing
prefabs
preface
prefaced
prefaces
prefacing
prefect
prefer
preferable
preferably
preference
preferences
preferential
preferred
preferring
prefers
prefix
prefixed
prefixes
prefixing
pregnancies
pregnancy
pregnant
prehistoric
prejudice
prejudiced
prejudices
prejudicial
prejudicing
preliminaries
preliminary
prelude
preludes
premature
prematurely
premeditation
premier
premiere
premiered
premieres
premiering
premiers
premise
premised
premises
premising
premiss
premisses
premium
premiums
premonition
premonitions
prenatal
preoccupied
preoccupies
preoccupy
preoccupying
prepaid
preparation
preparations
preparatory
prepare
prepared
prepares
preparing
prepay
prepaying
prepays
preponderance
preponderances
preposition
prepositional
prepositions
preposterous
prerequisite
prerequisites
prerogative
prerogatives
prescribe
prescribed
prescribes
prescribing
prescription
prescriptions
presence
presences
present
presentable
presentation
presentations
presented
presenter
presenting
presently
presents
preservation
preservative
preservatives
preserve
preserved
preserves
preserving
preside
presided
presidencies
presidency
president
presidential
presidents
presides
presiding
press
pressed
presses
pressing
pressings
pressure
pressured
pressures
pressuring
prestige
prestigious
presto
presumably
presume
presumed
presumes
presuming
presumption
presumptions
presumptuous
presuppose
presupposed
presupposes
presupposing
pretence
pretences
pretend
pretended
pretender
pretenders
pretending
pretends
pretense
pretenses
pretension
pretensions
pretentious
pretentiously
pretentiousness
pretext
pretexts
prettied
prettier
pretties
prettiest
pretty
prettying
pretzel
pretzels
prevail
prevailed
prevailing
prevails
prevalence
prevalent
prevent
preventable
prevented
preventible
preventing
prevention
preventive
preventives
prevents
preview
previewed
previewer
previewers
previewing
previews
previous
previously
prevue
prevues
prey
preyed
preying
preys
price
priced
priceless
prices
pricing
prick
pricked
pricking
prickle
prickled
prickles
pricklier
prickliest
prickling
prickly
pricks
pride
prided
prides
priding
pried
pries
priest
priestess
priestesses
priesthood
priesthoods
priests
prim
primaeval
primal
primaries
primarily
primary
primate
primates
prime
primed
primer
primers
primes
primeval
priming
primitive
primitives
primly
primmer
primmest
primp
primped
primping
primps
primrose
primroses
prince
princes
princess
princesses
principal
principalities
principality
principally
principals
principle
principles
print
printable
printed
printer
printers
printing
printings
printout
printouts
prints
prior
priorities
priority
priors
prism
prisms
prison
prisoner
prisoners
prisons
privacy
private
privately
privater
privates
privatest
privation
privations
privatization
privatize
privatized
privatizes
privatizing
privier
privies
priviest
privilege
privileged
privileges
privileging
privy
prize
prized
prizes
prizing
pro
probabilistic
probabilities
probability
probable
probables
probably
probation
probe
probed
probes
probing
problem
problematic
problems
procedural
procedure
procedures
proceed
proceeded
proceeding
proceedings
proceeds
process
processed
processes
processing
procession
processional
processionals
processioned
processioning
processions
processor
processors
proclaim
proclaimed
proclaiming
proclaims
proclamation
proclamations
procrastinate
procrastinated
procrastinates
procrastinating
procrastination
procure
procured
procurement
procures
procuring
prod
prodded
prodding
prodigal
prodigals
prodigies
prodigious
prodigy
prods
produce
produced
producer
producers
produces
producing
product
production
productions
productive
productivity
products
profane
profaned
profanes
profaning
profanities
profanity
profess
professed
professes
professing
profession
professional
professionally
professionals
professions
professor
professors
proffer
proffered
proffering
proffers
proficiency
proficient
proficiently
proficients
profile
profiled
profiles
profiling
profit
profitable
profited
profiteer
profiteered
profiteering
profiteers
profiting
profits
profound
profounder
profoundest
profoundly
profundities
profundity
profuse
profusely
profusion
profusions
progeny
prognoses
prognosis
program
programed
programer
programers
programing
programmable
programmed
programmer
programmers
programming
programs
progress
progressed
progresses
progressing
progression
progressions
progressive
progressively
progressives
prohibit
prohibited
prohibiting
prohibition
prohibitions
prohibitive
prohibitively
prohibits
project
projected
projectile
projectiles
projecting
projection
projections
projector
projectors
projects
proletarian
proletarians
proletariat
proliferate
proliferated
proliferates
proliferating
proliferation
prolific
prolog
prologs
prologue
prologues
prolong
prolonged
prolonging
prolongs
prom
promenade
promenaded
promenades
promenading
prominence
prominent
prominently
promiscuity
promiscuous
promise
promised
promises
promising
promontories
promontory
promote
promoted
promotes
promoting
promotion
promotions
prompt
prompted
prompter
promptest
prompting
promptly
promptness
prompts
proms
promulgate
promulgated
promulgates
promulgating
prone
prong
prongs
pronoun
pronounce
pronounced
pronouncement
pronouncements
pronounces
pronouncing
pronouns
pronunciation
pronunciations
proof
proofed
proofing
proofread
proofreading
proofreads
proofs
prop
propaganda
propagate
propagated
propagates
propagating
propagation
propel
propelled
propeller
propellers
propelling
propels
propensities
propensity
proper
properer
properest
properly
properties
property
prophecies
prophecy
prophesied
prophesies
prophesy
prophesying
prophet
prophetic
prophets
proponent
proponents
proportion
proportional
proportionality
proportionally
proportionals
proportionate
proportioned
proportioning
proportions
proposal
proposals
propose
proposed
proposes
proposing
proposition
propositional
propositioned
propositioning
propositions
propped
propping
proprietaries
proprietary
proprietor
proprietors
propriety
props
propulsion
pros
prose
prosecute
prosecuted
prosecutes
prosecuting
prosecution
prosecutions
prosecutor
prosecutors
prospect
prospected
prospecting
prospective
prospector
prospectors
prospects
prospectus
prospectuses
prosper
prospered
prospering
prosperity
prosperous
prospers
prostitute
prostituted
prostitutes
prostituting
prostitution
prostrate
prostrated
prostrates
prostrating
protagonist
protagonists
protect
protected
protecting
protection
protections
protective
protector
protectors
protects
protein
proteins
protest
protestant
protested
protesting
protestor
protestors
protests
protocol
protocols
proton
protons
prototype
prototypes
protract
protracted
protracting
protractor
protractors
protracts
protrude
protruded
protrudes
protruding
protrusion
protrusions
proud
prouder
proudest
proudly
provable
provably
prove
proved
proven
provenance
proverb
proverbial
proverbs
proves
provide
provided
providence
provider
provides
providing
province
provinces
provincial
provincials
proving
provision
provisional
provisionally
provisioned
provisioning
provisions
proviso
provisoes
provisos
provocation
provocations
provocative
provoke
provoked
provokes
provoking
prow
prowess
prowl
prowled
prowler
prowlers
prowling
prowls
prows
proxies
proximity
proxy
prude
prudence
prudent
prudes
prudish
prune
pruned
prunes
pruning
pry
prying
psalm
psalms
pseudo
pseudonym
pseudonyms
psych
psyche
psyched
psychedelic
psychedelics
psyches
psychiatric
psychiatrist
psychiatrists
psychiatry
psychic
psychics
psyching
psychoanalysis
psychoanalyst
psychoanalysts
psychological
psychologically
psychologies
psychologist
psychologists
psychology
psychopath
psychopaths
psychoses
psychosis
psychotherapies
psychotherapy
psychotic
psychs
pub
puberty
public
publication
publications
publicity
publicize
publicized
publicizes
publicizing
publicly
publish
published
publisher
publishers
publishes
publishing
puck
pucker
puckered
puckering
puckers
pucks
pudding
puddings
puddle
puddled
puddles
puddling
pudgier
pudgiest
pudgy
pueblo
pueblos
puff
puffed
puffer
puffier
puffiest
puffing
puffs
puffy
pugnacious
puke
puked
pukes
puking
pull
pulled
pulley
pulleys
pulling
pullover
pullovers
pulls
pulmonary
pulp
pulped
pulping
pulpit
pulpits
pulps
pulsate
pulsated
pulsates
pulsating
pulsation
pulsations
pulse
pulsed
pulses
pulsing
pulverize
pulverized
pulverizes
pulverizing
puma
pumas
pumice
pumices
pummel
pummeled
pummeling
pummelled
pummelling
pummels
pump
pumped
pumpernickel
pumping
pumpkin
pumpkins
pumps
pun
punch
punched
punches
punching
punchline
punctual
punctuality
punctuate
punctuated
punctuates
punctuating
punctuation
puncture
punctured
punctures
puncturing
pundit
pundits
pungent
punier
puniest
punish
punishable
punished
punishes
punishing
punishment
punishments
punitive
punk
punker
punkest
punks
punned
punning
puns
punt
punted
punter
punters
punting
punts
puny
pup
pupil
pupils
pupped
puppet
puppets
puppies
pupping
puppy
pups
purchase
purchased
purchaser
purchasers
purchases
purchasing
pure
puree
pureed
pureeing
purees
purely
purer
purest
purgatory
purge
purged
purges
purging
purification
purified
purifies
purify
purifying
puritanical
purity
purple
purpler
purples
purplest
purport
purported
purporting
purports
purpose
purposed
purposeful
purposes
purposing
purr
purred
purring
purrs
purse
pursed
purses
pursing
pursue
pursued
pursues
pursuing
pursuit
pursuits
purveyor
pus
push
pushed
pusher
pushers
pushes
pushier
pushiest
pushing
pushover
pushovers
pushy
puss
pusses
pussier
pussies
pussiest
pussy
put
putative
putrid
puts
putt
putted
putter
puttered
puttering
putters
puttied
putties
putting
putts
putty
puttying
puzzle
puzzled
puzzles
puzzling
pyramid
pyramided
pyramiding
pyramids
pyre
pyres
python
pythons
qua
quack
quacked
quacking
quacks
quadrangle
quadrangles
quadrant
quadrants
quadratic
quadrilateral
quadrilaterals
quadruped
quadrupeds
quadruple
quadrupled
quadruples
quadruplet
quadruplets
quadrupling
quagmire
quagmires
quail
quailed
quailing
quails
quaint
quainter
quaintest
quake
quaked
quakes
quaking
qualification
qualifications
qualified
qualifier
qualifiers
qualifies
qualify
qualifying
qualitative
qualities
quality
qualm
qualms
quandaries
quandary
quantifier
quantify
quantitative
quantities
quantity
quantum
quarantine
quarantined
quarantines
quarantining
quark
quarrel
quarreled
quarreling
quarrelled
quarrelling
quarrels
quarrelsome
quarried
quarries
quarry
quarrying
quart
quarter
quarterback
quarterbacked
quarterbacking
quarterbacks
quartered
quartering
quarterlies
quarterly
quarters
quartet
quartets
quartette
quartettes
quarts
quartz
quash
quashed
quashes
quashing
quaver
quavered
quavering
quavers
quay
quays
queasier
queasiest
queasy
queen
queened
queening
queenlier
queenliest
queenly
queens
queer
queered
queerer
queerest
queering
queers
quell
quelled
quelling
quells
quench
quenched
quenches
quenching
queried
queries
query
querying
quest
quested
questing
question
questionable
questioned
questioning
questionnaire
questionnaires
questions
quests
queue
queued
queues
queuing
quibble
quibbled
quibbles
quibbling
quiche
quick
quicken
quickened
quickening
quickens
quicker
quickest
quickly
quicksand
quicksands
quiet
quieted
quieter
quietest
quieting
quietly
quiets
quill
quills
quilt
quilted
quilting
quilts
quinine
quintessence
quintessences
quintet
quintets
quintuplet
quintuplets
quip
quipped
quipping
quips
quirk
quirked
quirking
quirks
quirky
quit
quite
quits
quitted
quitter
quitters
quitting
quiver
quivered
quivering
quivers
quiz
quizzed
quizzes
quizzical
quizzing
quorum
quorums
quota
quotas
quotation
quotations
quote
quoted
quotes
quotient
quotients
quoting
rabbi
rabbis
rabbit
rabbited
rabbiting
rabbits
rabble
rabbles
rabid
rabies
raccoon
raccoons
race
raced
racer
races
racetrack
racetracks
racial
racially
racier
raciest
racing
racism
racist
racists
rack
racked
racket
racketed
racketeer
racketeered
racketeering
racketeers
racketing
rackets
racking
racks
racoon
racoons
racquet
racquets
racy
radar
radars
radial
radials
radiance
radiant
radiate
radiated
radiates
radiating
radiation
radiations
radiator
radiators
radical
radically
radicals
radii
radio
radioactive
radioactivity
radioed
radioing
radios
radish
radishes
radium
radius
radiuses
raffle
raffled
raffles
raffling
raft
rafted
rafter
rafters
rafting
rafts
rag
ragamuffin
ragamuffins
rage
raged
rages
ragged
raggeder
raggedest
ragging
raging
rags
ragtime
raid
raided
raider
raiders
raiding
raids
rail
railed
railing
railings
railroad
railroaded
railroading
railroads
rails
railway
railways
rain
rainbow
rainbows
raincoat
raincoats
raindrop
raindrops
rained
rainfall
rainfalls
rainforest
rainier
rainiest
raining
rains
rainstorm
rainstorms
rainwater
rainy
raise
raised
raises
raisin
raising
raisins
rake
raked
rakes
raking
rallied
rallies
rally
rallying
ram
ramble
rambled
rambler
ramblers
rambles
rambling
ramification
ramifications
rammed
ramming
ramp
rampage
rampaged
rampages
rampaging
rampant
ramps
ramrod
ramrodded
ramrodding
ramrods
rams
ramshackle
ran
ranch
ranched
rancher
ranchers
ranches
ranching
rancid
rancor
rancorous
random
randomly
randomness
rang
range
ranged
ranger
rangers
ranges
ranging
rank
ranked
ranker
rankest
ranking
rankle
rankled
rankles
rankling
ranks
ransack
ransacked
ransacking
ransacks
ransom
ransomed
ransoming
ransoms
rant
ranted
ranting
rants
rap
rape
raped
rapes
rapid
rapider
rapidest
rapidity
rapidly
rapids
raping
rapist
rapists
rapped
rapping
rapport
rapports
raps
rapt
rapture
raptures
rapturous
rare
rared
rarely
rarer
rares
rarest
raring
rarities
rarity
rascal
rascals
rash
rasher
rashes
rashest
rashly
rasp
raspberries
raspberry
rasped
rasping
rasps
raster
rat
rate
rated
rates
rather
ratification
ratified
ratifies
ratify
ratifying
rating
ratings
ratio
ration
rational
rationale
rationales
rationality
rationalization
rationalize
rationalized
rationalizes
rationalizing
rationally
rationals
rationed
rationing
rations
ratios
rats
ratted
ratting
rattle
rattled
rattler
rattlers
rattles
rattlesnake
rattlesnakes
rattling
ratty
raucous
raucously
ravage
ravaged
ravages
ravaging
rave
raved
ravel
raveled
raveling
ravelled
ravelling
ravels
raven
ravened
ravening
ravenous
ravenously
ravens
raves
ravine
ravines
raving
ravings
ravish
ravished
ravishes
ravishing
raw
rawer
rawest
ray
rayon
rays
raze
razed
razes
razing
razor
razors
re
reach
reached
reaches
reaching
react
reacted
reacting
reaction
reactionaries
reactionary
reactions
reactive
reactor
reactors
reacts
read
readability
readable
reader
readers
readership
readied
readier
readies
readiest
readily
readiness
reading
readings
readjust
readjusted
readjusting
readjusts
reads
ready
readying
real
realer
reales
realest
realism
realist
realistic
realistically
realists
realities
reality
realization
realize
realized
realizes
realizing
reallocate
reallocated
reallocates
reallocating
really
realm
realms
reals
realty
ream
reamed
reaming
reams
reap
reaped
reaper
reapers
reaping
reappear
reappeared
reappearing
reappears
reaps
rear
reared
rearing
rearrange
rearranged
rearrangement
rearrangements
rearranges
rearranging
rears
reason
reasonable
reasonably
reasoned
reasoning
reasons
reassurance
reassurances
reassure
reassured
reassures
reassuring
rebate
rebated
rebates
rebating
rebel
rebelled
rebelling
rebellion
rebellions
rebellious
rebels
rebind
rebinding
rebinds
rebirth
rebirths
reborn
rebound
rebounded
rebounding
rebounds
rebuff
rebuffed
rebuffing
rebuffs
rebuild
rebuilding
rebuilds
rebuilt
rebuke
rebuked
rebukes
rebuking
rebut
rebuts
rebuttal
rebuttals
rebutted
rebutting
recalcitrant
recall
recalled
recalling
recalls
recant
recanted
recanting
recants
recap
recapped
recapping
recaps
recapture
recaptured
recaptures
recapturing
recede
receded
recedes
receding
receipt
receipted
receipting
receipts
receive
received
receiver
receivers
receives
receiving
recent
recenter
recentest
recently
receptacle
receptacles
reception
receptionist
receptionists
receptions
receptive
recess
recessed
recesses
recessing
recession
recessions
recharge
rechargeable
recharged
recharges
recharging
recipe
recipes
recipient
recipients
reciprocal
reciprocals
reciprocate
reciprocated
reciprocates
reciprocating
recital
recitals
recitation
recitations
recite
recited
recites
reciting
reckless
recklessly
recklessness
reckon
reckoned
reckoning
reckons
reclaim
reclaimed
reclaiming
reclaims
reclamation
recline
reclined
reclines
reclining
recluse
recluses
recognition
recognizable
recognize
recognized
recognizes
recognizing
recoil
recoiled
recoiling
recoils
recollect
recollected
recollecting
recollection
recollections
recollects
recommend
recommendation
recommendations
recommended
recommending
recommends
recompense
recompensed
recompenses
recompensing
recompile
recompiled
recompiling
reconcile
reconciled
reconciles
reconciliation
reconciliations
reconciling
recondition
reconditioned
reconditioning
reconditions
reconfigure
reconfigured
reconnaissance
reconnaissances
reconnect
reconnected
reconnecting
reconnects
reconsider
reconsidered
reconsidering
reconsiders
reconstruct
reconstructed
reconstructing
reconstruction
reconstructions
reconstructs
record
recorded
recorder
recorders
recording
recordings
records
recount
recounted
recounting
recounts
recoup
recouped
recouping
recoups
recourse
recover
recoverable
recovered
recoveries
recovering
recovers
recovery
recreate
recreated
recreates
recreating
recreation
recreational
recreations
recruit
recruited
recruiting
recruitment
recruits
recta
rectal
rectangle
rectangles
rectangular
rectified
rectifies
rectify
rectifying
rector
rectors
rectum
rectums
recuperate
recuperated
recuperates
recuperating
recuperation
recur
recurred
recurrence
recurrences
recurrent
recurring
recurs
recursion
recursive
recursively
recycle
recycled
recycles
recycling
red
redden
reddened
reddening
reddens
redder
reddest
redeem
redeemable
redeemed
redeeming
redeems
redefine
redefined
redefines
redefining
redefinition
redemption
redesign
redesigned
redesigning
redesigns
redhead
redheads
redid
redirect
redirected
redirecting
redirection
redirects
rediscover
rediscovered
rediscovering
rediscovers
redistribute
redistributed
redistributes
redistributing
redistribution
redo
redoes
redoing
redone
redraft
redraw
redress
redressed
redresses
redressing
reds
reduce
reduced
reduces
reducing
reduction
reductions
redundancies
redundancy
redundant
reed
reeds
reef
reefed
reefing
reefs
reek
reeked
reeking
reeks
reel
reelect
reelected
reelecting
reelects
reeled
reeling
reels
reenforce
reenforced
reenforces
reenforcing
refer
referee
refereed
refereeing
referees
reference
referenced
references
referencing
referenda
referendum
referendums
referred
referring
refers
refill
refilled
refilling
refills
refine
refined
refinement
refinements
refineries
refinery
refines
refining
reflect
reflected
reflecting
reflection
reflections
reflective
reflector
reflectors
reflects
reflex
reflexes
reflexive
reflexives
reform
reformat
reformation
reformations
reformatted
reformatting
reformed
reformer
reformers
reforming
reforms
refraction
refrain
refrained
refraining
refrains
refresh
refreshed
refreshes
refreshing
refreshment
refreshments
refrigerate
refrigerated
refrigerates
refrigerating
refrigeration
refrigerator
refrigerators
refuel
refueled
refueling
refuelled
refuelling
refuels
refuge
refugee
refugees
refuges
refund
refunded
refunding
refunds
refurbish
refurbished
refurbishes
refurbishing
refurbishment
refusal
refusals
refuse
refused
refuses
refusing
refutation
refute
refuted
refutes
refuting
regain
regained
regaining
regains
regal
regale
regaled
regales
regalia
regaling
regard
regarded
regarding
regardless
regards
regatta
regattas
regenerate
regenerated
regenerates
regenerating
regeneration
regent
regents
regime
regimen
regimens
regiment
regimental
regimented
regimenting
regiments
regimes
region
regional
regions
register
registered
registering
registers
registrar
registrars
registration
registrations
registries
registry
regress
regressed
regresses
regressing
regression
regressions
regret
regretful
regrets
regrettable
regrettably
regretted
regretting
regular
regularity
regularly
regulars
regulate
regulated
regulates
regulating
regulation
regulations
regurgitate
regurgitated
regurgitates
regurgitating
rehabilitate
rehabilitated
rehabilitates
rehabilitating
rehabilitation
rehash
rehashed
rehashes
rehashing
rehearsal
rehearsals
rehearse
rehearsed
rehearses
rehearsing
reign
reigned
reigning
reigns
reimburse
reimbursed
reimbursement
reimbursements
reimburses
reimbursing
rein
reincarnate
reincarnated
reincarnates
reincarnating
reincarnation
reincarnations
reindeer
reindeers
reined
reinforce
reinforced
reinforcement
reinforcements
reinforces
reinforcing
reining
reins
reinstate
reinstated
reinstatement
reinstates
reinstating
reis
reiterate
reiterated
reiterates
reiterating
reiteration
reiterations
reject
rejected
rejecting
rejection
rejections
rejects
rejoice
rejoiced
rejoices
rejoicing
rejoin
rejoinder
rejoinders
rejoined
rejoining
rejoins
rejuvenate
rejuvenated
rejuvenates
rejuvenating
rejuvenation
relaid
relapse
relapsed
relapses
relapsing
relate
related
relates
relating
relation
relational
relations
relationship
relationships
relative
relatively
relatives
relativistic
relativity
relax
relaxation
relaxations
relaxed
relaxes
relaxing
relay
relayed
relaying
relays
releasable
release
released
releases
releasing
relegate
relegated
relegates
relegating
relent
relented
relenting
relentless
relentlessly
relents
relevance
relevant
reliability
reliable
reliably
reliance
reliant
relic
relics
relied
relief
reliefs
relies
relieve
relieved
relieves
relieving
religion
religions
religious
religiously
relinquish
relinquished
relinquishes
relinquishing
relish
relished
relishes
relishing
relive
relived
relives
reliving
reload
reloaded
reloading
reloads
relocatable
relocate
relocated
relocates
relocating
relocation
reluctance
reluctant
reluctantly
rely
relying
remade
remain
remainder
remainders
remained
remaining
remains
remake
remakes
remaking
remark
remarkable
remarkably
remarked
remarking
remarks
remedial
remedied
remedies
remedy
remedying
remember
remembered
remembering
remembers
remembrance
remembrances
remind
reminded
reminder
reminders
reminding
reminds
reminisce
reminisced
reminiscence
reminiscences
reminiscent
reminisces
reminiscing
remiss
remission
remissions
remit
remits
remittance
remittances
remitted
remitting
remnant
remnants
remodel
remodeled
remodeling
remodelled
remodelling
remodels
remorse
remorseful
remorseless
remote
remotely
remoter
remotes
remotest
removable
removal
removals
remove
removed
removes
removing
remunerate
remunerated
remunerates
remunerating
remuneration
remunerations
renaissance
rename
renamed
renames
renaming
rend
render
rendered
rendering
renders
rendezvous
rendezvoused
rendezvouses
rendezvousing
rending
rendition
renditions
rends
renegade
renegaded
renegades
renegading
renege
reneged
reneges
reneging
renew
renewable
renewal
renewals
renewed
renewing
renews
renounce
renounced
renounces
renouncing
renovate
renovated
renovates
renovating
renovation
renovations
renown
renowned
rent
rental
rentals
rented
renting
rents
renunciation
renunciations
reopen
reopened
reopening
reopens
reorganization
reorganize
reorganized
reorganizes
reorganizing
repaid
repair
repaired
repairing
repairs
reparation
repatriate
repatriated
repatriates
repatriating
repay
repaying
repayment
repayments
repays
repeal
repealed
repealing
repeals
repeat
repeatable
repeated
repeatedly
repeating
repeats
repel
repellant
repellants
repelled
repellent
repellents
repelling
repels
repent
repentance
repentant
repented
repenting
repents
repercussion
repercussions
repertoire
repertoires
repetition
repetitions
repetitious
repetitive
rephrase
replace
replaced
replacement
replacements
replaces
replacing
replay
replenish
replenished
replenishes
replenishing
replete
repleted
repletes
repleting
replica
replicas
replicate
replicated
replicates
replicating
replication
replied
replies
reply
replying
report
reported
reportedly
reporter
reporters
reporting
reports
repose
reposed
reposes
reposing
repositories
repository
reprehensible
represent
representation
representations
representative
representatives
represented
representing
represents
repress
repressed
represses
repressing
repression
repressions
repressive
reprieve
reprieved
reprieves
reprieving
reprimand
reprimanded
reprimanding
reprimands
reprint
reprinted
reprinting
reprints
reprisal
reprisals
reproach
reproached
reproaches
reproaching
reproduce
reproduced
reproduces
reproducing
reproduction
reproductions
reproductive
reprogram
reprogramed
reprograming
reprogrammed
reprogramming
reprograms
reprove
reproved
reproves
reproving
reptile
reptiles
republic
republican
republicans
republics
repudiate
repudiated
repudiates
repudiating
repudiation
repudiations
repugnance
repugnant
repulse
repulsed
repulses
repulsing
repulsion
repulsive
reputable
reputation
reputations
repute
reputed
reputedly
reputes
reputing
request
requested
requesting
requests
requiem
require
required
requirement
requirements
requires
requiring
requisite
requisites
requisition
requisitioned
requisitioning
requisitions
reread
rereading
rereads
reroute
rerouted
reroutes
rerouting
resale
reschedule
rescheduled
reschedules
rescheduling
rescind
rescinded
rescinding
rescinds
rescue
rescued
rescuer
rescuers
rescues
rescuing
research
researched
researcher
researchers
researches
researching
resemblance
resemblances
resemble
resembled
resembles
resembling
resent
resented
resentful
resenting
resentment
resentments
resents
reservation
reservations
reserve
reserved
reserves
reserving
reservoir
reservoirs
reset
resets
resetting
reshuffle
reside
resided
residence
residences
resident
residential
residents
resides
residing
residual
residuals
residue
residues
resign
resignation
resignations
resigned
resigning
resigns
resilience
resilient
resin
resins
resist
resistance
resistances
resistant
resisted
resisting
resistor
resistors
resists
resolute
resolutely
resolution
resolutions
resolve
resolved
resolver
resolves
resolving
resonance
resonances
resonant
resort
resorted
resorting
resorts
resound
resounded
resounding
resounds
resource
resourced
resourceful
resourcefulness
resources
resourcing
respect
respectability
respectable
respectably
respected
respectful
respectfully
respecting
respective
respectively
respects
respiration
respirator
respirators
respiratory
respite
respites
resplendent
respond
responded
responding
responds
response
responses
responsibilities
responsibility
responsible
responsibly
responsive
rest
restart
restarted
restarting
restarts
restaurant
restaurants
rested
restful
restfuller
restfullest
resting
restitution
restive
restless
restlessly
restlessness
restoration
restorations
restore
restored
restores
restoring
restrain
restrained
restraining
restrains
restraint
restraints
restrict
restricted
restricting
restriction
restrictions
restrictive
restricts
restructure
restructured
restructures
restructuring
rests
resubmit
resubmits
resubmitted
resubmitting
result
resultant
resultants
resulted
resulting
results
resume
resumed
resumes
resuming
resumption
resumptions
resurface
resurfaced
resurfaces
resurfacing
resurgence
resurgences
resurrect
resurrected
resurrecting
resurrection
resurrections
resurrects
resuscitate
resuscitated
resuscitates
resuscitating
resuscitation
retail
retailed
retailer
retailers
retailing
retails
retain
retained
retainer
retainers
retaining
retains
retaliate
retaliated
retaliates
retaliating
retaliation
retaliations
retard
retarded
retarding
retards
retch
retched
retches
retching
retention
rethink
reticence
reticent
retina
retinae
retinas
retire
retired
retirement
retirements
retires
retiring
retort
retorted
retorting
retorts
retrace
retraced
retraces
retracing
retract
retracted
retracting
retraction
retractions
retracts
retreat
retreated
retreating
retreats
retribution
retributions
retries
retrieval
retrievals
retrieve
retrieved
retriever
retrievers
retrieves
retrieving
retroactive
retrograde
retrospect
retrospected
retrospecting
retrospective
retrospectively
retrospectives
retrospects
retry
return
returnable
returnables
returned
returning
returns
retype
reunion
reunions
reunite
reunited
reunites
reuniting
reuse
reused
reuses
reusing
rev
revamp
revamped
revamping
revamps
reveal
revealed
revealing
reveals
revel
revelation
revelations
reveled
reveler
revelers
reveling
revelled
reveller
revellers
revelling
revelries
revelry
revels
revenge
revenged
revengeful
revenges
revenging
revenue
revenues
reverberate
reverberated
reverberates
reverberating
reverberation
reverberations
revere
revered
reverence
reverenced
reverences
reverencing
reverent
reverently
reveres
reverie
reveries
revering
reversal
reversals
reverse
reversed
reverses
reversible
reversing
reversion
revert
reverted
reverting
reverts
revery
review
reviewed
reviewer
reviewers
reviewing
reviews
revile
reviled
reviles
reviling
revise
revised
revises
revising
revision
revisions
revisit
revisited
revisiting
revisits
revival
revivals
revive
revived
revives
reviving
revoke
revoked
revokes
revoking
revolt
revolted
revolting
revolts
revolution
revolutionaries
revolutionary
revolutionize
revolutionized
revolutionizes
revolutionizing
revolutions
revolve
revolved
revolver
revolvers
revolves
revolving
revs
revue
revues
revulsion
revved
revving
reward
rewarded
rewarding
rewards
rewind
rework
rewrite
rewrites
rewriting
rewritten
rewrote
rhapsodies
rhapsody
rhetoric
rhetorical
rheumatism
rhino
rhinoceri
rhinoceros
rhinoceroses
rhinos
rhododendron
rhododendrons
rhubarb
rhubarbs
rhyme
rhymed
rhymes
rhyming
rhythm
rhythmic
rhythms
rib
ribbed
ribbing
ribbon
ribbons
ribs
rice
riced
rices
rich
richer
riches
richest
richly
richness
ricing
ricketier
ricketiest
rickety
ricksha
rickshas
rickshaw
rickshaws
ricochet
ricocheted
ricocheting
ricochets
ricochetted
ricochetting
rid
riddance
ridded
ridden
ridding
riddle
riddled
riddles
riddling
ride
rider
riders
rides
ridge
ridged
ridges
ridging
ridicule
ridiculed
ridicules
ridiculing
ridiculous
ridiculously
riding
rids
rife
rifer
rifest
rifle
rifled
rifles
rifling
rift
rifted
rifting
rifts
rig
rigged
rigging
right
righted
righteous
righteously
righteousness
righter
rightest
rightful
rightfully
righting
rightly
rightmost
rightness
rights
rigid
rigidity
rigidly
rigor
rigorous
rigorously
rigors
rigs
rile
riled
riles
riling
rim
rimmed
rimming
rims
rind
rinds
ring
ringed
ringing
ringleader
ringleaders
ringlet
ringlets
rings
ringworm
rink
rinks
rinse
rinsed
rinses
rinsing
riot
rioted
rioter
rioters
rioting
riotous
riots
rip
ripe
ripen
ripened
ripeness
ripening
ripens
riper
ripest
riposte
ripped
ripping
ripple
rippled
ripples
rippling
rips
rise
risen
riser
risers
rises
rising
risk
risked
riskier
riskiest
risking
risks
risky
rite
rites
ritual
rituals
rival
rivaled
rivaling
rivalled
rivalling
rivalries
rivalry
rivals
river
rivers
rivet
riveted
riveting
rivets
rivetted
rivetting
roach
roaches
road
roadblock
roadblocked
roadblocking
roadblocks
roads
roadside
roadsides
roam
roamed
roaming
roams
roar
roared
roaring
roars
roast
roasted
roasting
roasts
rob
robbed
robber
robberies
robbers
robbery
robbing
robe
robed
robes
robin
robing
robins
robot
robots
robs
robust
robuster
robustest
robustness
rock
rocked
rocker
rockers
rocket
rocketed
rocketing
rockets
rockier
rockiest
rocking
rocks
rocky
rod
rode
rodent
rodents
rodeo
rodeos
rods
roe
roes
rogue
rogues
roguish
role
roles
roll
rolled
roller
rollers
rolling
rolls
roman
romance
romanced
romances
romancing
romantic
romantically
romantics
romp
romped
romping
romps
roof
roofed
roofing
roofs
rook
rooked
rookie
rookies
rooking
rooks
room
roomed
roomier
roomiest
rooming
roommate
roommates
rooms
roomy
roost
roosted
rooster
roosters
roosting
roosts
root
rooted
rooter
rooting
roots
rope
roped
ropes
roping
rosaries
rosary
rose
rosemary
roses
rosier
rosiest
roster
rosters
rostra
rostrum
rostrums
rosy
rot
rotaries
rotary
rotate
rotated
rotates
rotating
rotation
rotations
rote
rotisserie
rotisseries
rotor
rotors
rots
rotted
rotten
rottener
rottenest
rotting
rotund
rotunda
rotundas
rouge
rouged
rouges
rough
roughage
roughed
roughen
roughened
roughening
roughens
rougher
roughest
roughhouse
roughhoused
roughhouses
roughhousing
roughing
roughly
roughness
roughs
rouging
roulette
round
roundabout
roundabouts
rounded
rounder
roundest
rounding
roundness
rounds
rouse
roused
rouses
rousing
rout
route
routed
routeing
router
routes
routine
routinely
routines
routing
routs
row
rowboat
rowboats
rowdier
rowdies
rowdiest
rowdiness
rowdy
rowed
rowing
rows
royal
royally
royals
royalties
royalty
rub
rubbed
rubber
rubbers
rubbing
rubbish
rubbished
rubbishes
rubbishing
rubble
rubier
rubies
rubiest
rubric
rubs
ruby
rucksack
ruckus
ruckuses
rudder
rudders
ruddier
ruddiest
ruddy
rude
rudely
rudeness
ruder
rudest
rudimentary
rue
rued
rueful
rues
ruff
ruffed
ruffian
ruffians
ruffing
ruffle
ruffled
ruffles
ruffling
ruffs
rug
rugby
rugged
ruggeder
ruggedest
rugs
ruin
ruined
ruing
ruining
ruinous
ruins
rule
ruled
ruler
rulers
rules
ruling
rulings
rum
rumble
rumbled
rumbles
rumbling
ruminate
ruminated
ruminates
ruminating
rummage
rummaged
rummages
rummaging
rummer
rummest
rummy
rumor
rumored
rumoring
rumors
rump
rumple
rumpled
rumples
rumpling
rumps
rums
run
runaway
runaways
rundown
rundowns
rune
runes
rung
rungs
runner
runners
runnier
runniest
running
runny
runs
runt
runts
runway
runways
rupture
ruptured
ruptures
rupturing
rural
ruse
ruses
rush
rushed
rushes
rushing
rust
rusted
rustic
rustics
rustier
rustiest
rusting
rustle
rustled
rustler
rustlers
rustles
rustling
rusts
rusty
rut
ruthless
ruthlessly
ruthlessness
ruts
rutted
rutting
rye
sabbatical
saber
sabers
sabotage
sabotaged
sabotages
sabotaging
saboteur
saboteurs
sabre
sabres
sac
sack
sacked
sacking
sacks
sacrament
sacraments
sacred
sacrifice
sacrificed
sacrifices
sacrificial
sacrificing
sacrilege
sacrileges
sacrilegious
sacs
sad
sadden
saddened
saddening
saddens
sadder
saddest
saddle
saddled
saddles
saddling
sades
sadism
sadist
sadistic
sadists
sadly
sadness
safari
safaried
safariing
safaris
safe
safeguard
safeguarded
safeguarding
safeguards
safekeeping
safely
safer
safes
safest
safeties
safety
saffron
saffrons
sag
saga
sagas
sage
sagebrush
sager
sages
sagest
sagged
sagging
sags
said
sail
sailboat
sailboats
sailed
sailing
sailor
sailors
sails
saint
saintlier
saintliest
saintly
saints
sake
saki
salable
salad
salads
salami
salamis
salaries
salary
sale
saleable
sales
salesman
salesmen
salespeople
salesperson
salespersons
saleswoman
saleswomen
salient
salients
saliva
salivate
salivated
salivates
salivating
sallow
sallower
sallowest
sally
salmon
salmons
salon
salons
saloon
saloons
salt
salted
salter
saltest
saltier
saltiest
salting
salts
salty
salutation
salutations
salute
saluted
salutes
saluting
salvage
salvaged
salvages
salvaging
salvation
salve
salved
salves
salving
same
sameness
sames
sample
sampled
sampler
samples
sampling
sanatoria
sanatorium
sanatoriums
sanctified
sanctifies
sanctify
sanctifying
sanctimonious
sanction
sanctioned
sanctioning
sanctions
sanctity
sanctuaries
sanctuary
sand
sandal
sandals
sandbag
sandbagged
sandbagging
sandbags
sanded
sandier
sandiest
sanding
sandman
sandmen
sandpaper
sandpapered
sandpapering
sandpapers
sands
sandstone
sandstorm
sandstorms
sandwich
sandwiched
sandwiches
sandwiching
sandy
sane
saner
sanest
sang
sangs
sanitaria
sanitarium
sanitariums
sanitary
sanitation
sanity
sank
sanserif
sap
sapling
saplings
sapped
sapphire
sapphires
sapping
saps
sarcasm
sarcasms
sarcastic
sarcastically
sardine
sardines
saree
sarees
sari
saris
sash
sashes
sassier
sassiest
sassy
sat
satanic
satchel
satchels
satellite
satellited
satellites
satelliting
satin
satire
satires
satirical
satirist
satirists
satirize
satirized
satirizes
satirizing
satisfaction
satisfactions
satisfactorily
satisfactory
satisfied
satisfies
satisfy
satisfying
saturate
saturated
saturates
saturating
saturation
sauce
sauced
saucepan
saucepans
saucer
saucers
sauces
saucier
sauciest
saucing
saucy
sauerkraut
sauna
saunaed
saunaing
saunas
saunter
sauntered
sauntering
saunters
sausage
sausages
sauted
savage
savaged
savagely
savager
savageries
savagery
savages
savagest
savaging
save
saved
saver
saves
saving
savings
savior
saviors
saviour
saviours
savor
savored
savorier
savories
savoriest
savoring
savors
savory
savvied
savvier
savvies
savviest
savvy
savvying
saw
sawdust
sawed
sawing
sawn
saws
saxophone
saxophones
say
saying
sayings
says
scab
scabbed
scabbing
scabs
scaffold
scaffolding
scaffolds
scalar
scalars
scald
scalded
scalding
scalds
scale
scaled
scales
scalier
scaliest
scaling
scallop
scalloped
scalloping
scallops
scalp
scalped
scalpel
scalpels
scalping
scalps
scaly
scamper
scampered
scampering
scampers
scan
scandal
scandalize
scandalized
scandalizes
scandalizing
scandalous
scandals
scanned
scanner
scanners
scanning
scans
scant
scanted
scanter
scantest
scantier
scanties
scantiest
scanting
scants
scanty
scapegoat
scapegoated
scapegoating
scapegoats
scar
scarce
scarcely
scarcer
scarcest
scarcity
scare
scarecrow
scarecrows
scared
scares
scarf
scarfed
scarfing
scarfs
scarier
scariest
scaring
scarlet
scarred
scarring
scars
scarves
scary
scathing
scatter
scatterbrain
scatterbrained
scatterbrains
scattered
scattering
scatters
scavenger
scavengers
scenario
scenarios
scene
scenery
scenes
scenic
scent
scented
scenting
scents
scepter
scepters
schedule
scheduled
scheduler
schedules
scheduling
scheme
schemed
schemer
schemers
schemes
scheming
schizophrenia
schizophrenic
scholar
scholarly
scholars
scholarship
scholarships
scholastic
school
schoolboy
schoolboys
schoolchild
schoolchildren
schooled
schooling
schools
schoolteacher
schoolteachers
schooner
schooners
science
sciences
scientific
scientifically
scientist
scientists
scissor
scissors
scoff
scoffed
scoffing
scoffs
scold
scolded
scolding
scolds
scollop
scolloped
scolloping
scollops
scoop
scooped
scooping
scoops
scoot
scooted
scooter
scooters
scooting
scoots
scope
scoped
scopes
scoping
scorch
scorched
scorches
scorching
score
scored
scorer
scores
scoring
scorn
scorned
scornful
scorning
scorns
scorpion
scorpions
scotch
scotches
scotchs
scoundrel
scoundrels
scour
scoured
scourge
scourged
scourges
scourging
scouring
scours
scout
scouted
scouting
scouts
scowl
scowled
scowling
scowls
scrabble
scram
scramble
scrambled
scrambles
scrambling
scrammed
scramming
scrams
scrap
scrapbook
scrapbooks
scrape
scraped
scrapes
scraping
scrapped
scrapping
scraps
scratch
scratched
scratches
scratchier
scratchiest
scratching
scratchy
scrawl
scrawled
scrawling
scrawls
scrawnier
scrawniest
scrawny
scream
screamed
screaming
screams
screech
screeched
screeches
screeching
screen
screened
screening
screens
screw
screwdriver
screwdrivers
screwed
screwier
screwiest
screwing
screws
screwy
scribble
scribbled
scribbles
scribbling
scribe
scribes
script
scripted
scripting
scripts
scripture
scriptures
scriptwriter
scriptwriters
scroll
scrolled
scrolling
scrolls
scrounge
scrounged
scrounges
scrounging
scrub
scrubbed
scrubbing
scrubs
scruff
scruffier
scruffiest
scruffs
scruffy
scruple
scrupled
scruples
scrupling
scrupulous
scrupulously
scrutinize
scrutinized
scrutinizes
scrutinizing
scrutiny
scuff
scuffed
scuffing
scuffle
scuffled
scuffles
scuffling
scuffs
sculptor
sculptors
sculpture
sculptured
sculptures
sculpturing
scum
scummed
scumming
scums
scurried
scurries
scurrilous
scurry
scurrying
scuttle
scuttled
scuttles
scuttling
scythe
scythed
scythes
scything
sea
seafaring
seafood
seal
sealed
sealing
seals
seam
seaman
seamed
seamen
seaming
seams
seamstress
seamstresses
seaport
seaports
sear
search
searched
searches
searching
searchlight
searchlights
seared
searing
sears
seas
seashell
seashells
seashore
seashores
seasick
seasickness
seaside
seasides
season
seasonable
seasonal
seasoned
seasoning
seasonings
seasons
seat
seated
seating
seats
seaweed
secede
seceded
secedes
seceding
secession
seclude
secluded
secludes
secluding
seclusion
second
secondaries
secondarily
secondary
seconded
seconding
secondly
seconds
secrecy
secret
secretarial
secretaries
secretary
secrete
secreted
secretes
secreting
secretion
secretions
secretive
secretly
secrets
sect
section
sectioned
sectioning
sections
sector
sectors
sects
secular
secure
secured
securely
securer
secures
securest
securing
securities
security
sedan
sedans
sedate
sedated
sedater
sedates
sedatest
sedating
sedative
sedatives
sedentary
sediment
sedimentary
sediments
seduce
seduced
seduces
seducing
seduction
seductions
seductive
see
seed
seeded
seedier
seediest
seeding
seedling
seedlings
seeds
seedy
seeing
seek
seeking
seeks
seem
seemed
seeming
seemingly
seems
seen
seep
seepage
seeped
seeping
seeps
seer
sees
seesaw
seesawed
seesawing
seesaws
seethe
seethed
seethes
seething
segment
segmentation
segmented
segmenting
segments
segregate
segregated
segregates
segregating
segregation
seize
seized
seizes
seizing
seizure
seizures
seldom
select
selected
selecting
selection
selections
selective
selectively
selector
selectors
selects
self
selfish
selfishness
sell
seller
sellers
selling
sells
selves
semantic
semantically
semantics
semblance
semblances
semen
semester
semesters
semicircle
semicircles
semicolon
semicolons
semiconductor
semiconductors
semifinal
semifinals
seminar
seminaries
seminars
seminary
senate
senates
senator
senators
send
sender
sending
sends
senile
senility
senior
seniority
seniors
sensation
sensational
sensationalism
sensations
sense
sensed
senseless
senses
sensibilities
sensibility
sensible
sensibly
sensing
sensitive
sensitives
sensitivities
sensitivity
sensor
sensors
sensory
sensual
sensuality
sensuous
sent
sentence
sentenced
sentences
sentencing
sentience
sentient
sentiment
sentimental
sentimentality
sentiments
sentries
sentry
separate
separated
separately
separates
separating
separation
separations
separator
separators
sepulcher
sepulchered
sepulchering
sepulchers
sequel
sequels
sequence
sequenced
sequencer
sequences
sequencing
sequential
sequentially
sequin
sequins
sera
serenade
serenaded
serenades
serenading
serene
serener
serenest
serenity
sergeant
sergeants
serial
serials
series
serious
seriously
seriousness
sermon
sermons
serpent
serpents
serum
serums
servant
servants
serve
served
server
servers
serves
service
serviceable
serviced
serviceman
servicemen
services
servicing
serviette
serviettes
servile
serving
servitude
session
sessions
set
setback
setbacks
sets
settable
setter
setters
setting
settings
settle
settled
settlement
settlements
settler
settlers
settles
settling
seven
sevens
seventeen
seventeens
seventeenth
seventeenths
seventh
sevenths
seventies
seventy
sever
several
severance
severances
severe
severed
severely
severer
severest
severing
severity
severs
sew
sewage
sewed
sewer
sewers
sewing
sewn
sews
sex
sexed
sexes
sexing
sexism
sexist
sexual
sexuality
sexually
sexy
shabbier
shabbiest
shabbily
shabby
shack
shackle
shackled
shackles
shackling
shacks
shade
shaded
shades
shadier
shadiest
shading
shadow
shadowed
shadowier
shadowiest
shadowing
shadows
shadowy
shady
shaft
shafted
shafting
shafts
shaggier
shaggiest
shaggy
shaikh
shaikhs
shake
shaken
shakes
shakier
shakiest
shaking
shaky
shall
shallow
shallower
shallowest
shallows
sham
shamble
shambles
shame
shamed
shameful
shamefully
shameless
shames
shaming
shammed
shamming
shampoo
shampooed
shampooing
shampoos
shamrock
shamrocks
shams
shanties
shanty
shape
shaped
shapelier
shapeliest
shapely
shapes
shaping
share
shared
shareholder
shareholders
shares
sharing
shark
sharked
sharking
sharks
sharp
sharped
sharpen
sharpened
sharpener
sharpeners
sharpening
sharpens
sharper
sharpest
sharping
sharply
sharpness
sharps
shatter
shattered
shattering
shatters
shave
shaved
shaven
shaver
shavers
shaves
shaving
shawl
shawls
shaykh
shaykhs
she
sheaf
shear
sheared
shearing
shears
sheath
sheathe
sheathed
sheathes
sheathing
sheaths
sheave
sheaves
shed
shedding
sheds
sheen
sheep
sheepish
sheepishly
sheer
sheered
sheerer
sheerest
sheering
sheers
sheet
sheets
sheik
sheikh
sheikhs
sheiks
shelf
shell
shelled
sheller
shellfish
shellfishes
shelling
shells
shelter
sheltered
sheltering
shelters
shelve
shelved
shelves
shelving
shepherd
shepherded
shepherding
shepherds
sherbert
sherberts
sherbet
sherbets
sheriff
sheriffs
sherries
sherry
shes
shied
shield
shielded
shielding
shields
shies
shift
shifted
shiftier
shiftiest
shifting
shiftless
shifts
shifty
shimmer
shimmered
shimmering
shimmers
shin
shine
shined
shines
shingle
shingled
shingles
shingling
shinier
shiniest
shining
shinned
shinning
shins
shiny
ship
shipment
shipments
shipped
shipping
ships
shipshape
shipwreck
shipwrecked
shipwrecking
shipwrecks
shire
shirk
shirked
shirking
shirks
shirt
shirted
shirting
shirts
shiver
shivered
shivering
shivers
shoal
shoaled
shoaling
shoals
shock
shocked
shocking
shocks
shod
shodden
shoddier
shoddiest
shoddy
shoe
shoed
shoeing
shoelace
shoelaces
shoes
shoestring
shoestrings
shone
shoo
shooed
shooing
shook
shoon
shoos
shoot
shooting
shoots
shop
shopkeeper
shopkeepers
shoplifter
shoplifters
shopped
shopper
shoppers
shopping
shops
shore
shored
shores
shoring
shorn
short
shortage
shortages
shortcoming
shortcomings
shorted
shorten
shortened
shortening
shortenings
shortens
shorter
shortest
shortfall
shorthand
shorting
shortlist
shortly
shortness
shorts
shot
shotgun
shotgunned
shotgunning
shotguns
shots
should
shoulder
shouldered
shouldering
shoulders
shout
shouted
shouting
shouts
shove
shoved
shovel
shoveled
shoveling
shovelled
shovelling
shovels
shoves
shoving
show
showcase
showcased
showcases
showcasing
showdown
showdowns
showed
shower
showered
showering
showers
showier
showiest
showing
showings
showman
showmen
shown
shows
showy
shrank
shrapnel
shred
shredded
shredding
shreds
shrew
shrewd
shrewder
shrewdest
shrewdness
shrews
shriek
shrieked
shrieking
shrieks
shrill
shrilled
shriller
shrillest
shrilling
shrills
shrimp
shrimped
shrimping
shrimps
shrine
shrines
shrink
shrinkage
shrinking
shrinks
shrivel
shriveled
shriveling
shrivelled
shrivelling
shrivels
shroud
shrouded
shrouding
shrouds
shrub
shrubberies
shrubbery
shrubs
shrug
shrugged
shrugging
shrugs
shrunk
shrunken
shuck
shucked
shucking
shucks
shudder
shuddered
shuddering
shudders
shuffle
shuffled
shuffles
shuffling
shun
shunned
shunning
shuns
shunt
shunted
shunting
shunts
shut
shutdown
shuts
shutter
shuttered
shuttering
shutters
shutting
shuttle
shuttled
shuttles
shuttling
shy
shyer
shyest
shying
shyness
sibling
siblings
sic
sick
sicked
sicken
sickened
sickening
sickens
sicker
sickest
sicking
sickle
sickles
sicklier
sickliest
sickly
sickness
sicknesses
sicks
sics
side
sided
sideline
sidelined
sidelines
sidelining
sidelong
sides
sideshow
sideshows
sidestep
sidestepped
sidestepping
sidesteps
sidetrack
sidetracked
sidetracking
sidetracks
sidewalk
sidewalks
sideways
siding
sidings
sidle
sidled
sidles
sidling
siege
sieges
sierra
siesta
siestas
sieve
sieved
sieves
sieving
sift
sifted
sifting
sifts
sigh
sighed
sighing
sighs
sight
sighted
sighting
sightless
sights
sigma
sign
signal
signaled
signaling
signalled
signalling
signals
signature
signatures
signed
signer
significance
significant
significantly
signified
signifies
signify
signifying
signing
signpost
signposted
signposting
signposts
signs
silence
silenced
silences
silencing
silent
silenter
silentest
silently
silents
silhouette
silhouetted
silhouettes
silhouetting
silicon
silk
silken
silks
sill
sillier
sillies
silliest
silliness
sills
silly
silo
silos
silt
silted
silting
silts
silver
silvered
silvering
silvers
silversmith
silversmiths
silverware
silvery
similar
similarities
similarity
similarly
simile
similes
simmer
simmered
simmering
simmers
simple
simpler
simplest
simplex
simplicity
simplification
simplified
simplifies
simplify
simplifying
simplistic
simply
simulate
simulated
simulates
simulating
simulation
simulations
simulator
simultaneous
simultaneously
sin
since
sincere
sincerely
sincerer
sincerest
sincerity
sine
sinew
sinews
sinewy
sinful
sing
singe
singed
singeing
singer
singers
singes
singing
single
singled
singles
singling
singly
sings
singular
singularity
singularly
singulars
sinister
sink
sinking
sinks
sinned
sinner
sinners
sinning
sins
sinus
sinuses
sip
siphon
siphoned
siphoning
siphons
sipped
sipping
sips
sir
sire
sired
siren
sirens
sires
siring
sirloin
sirloins
sirs
sirup
sirups
sissier
sissies
sissiest
sissy
sister
sisterhood
sisterhoods
sisterly
sisters
sit
site
sited
sites
siting
sits
sitter
sitters
sitting
situate
situated
situates
situating
situation
situations
six
sixes
sixpence
sixpences
sixteen
sixteens
sixteenth
sixteenths
sixth
sixths
sixties
sixtieth
sixtieths
sixty
sizable
size
sizeable
sized
sizer
sizes
sizing
sizzle
sizzled
sizzles
sizzling
skate
skateboard
skateboarded
skateboarding
skateboards
skated
skater
skaters
skates
skating
skein
skeins
skeleton
skeletons
skeptic
skeptical
skepticism
skeptics
sketch
sketched
sketches
sketchier
sketchiest
sketching
sketchy
skew
skewed
skewer
skewered
skewering
skewers
skewing
skews
ski
skid
skidded
skidding
skids
skied
skies
skiing
skill
skilled
skillet
skillets
skillful
skills
skim
skimmed
skimming
skimp
skimped
skimpier
skimpiest
skimping
skimps
skimpy
skims
skin
skinflint
skinflints
skinned
skinnier
skinniest
skinning
skinny
skins
skip
skipped
skipper
skippered
skippering
skippers
skipping
skips
skirmish
skirmished
skirmishes
skirmishing
skirt
skirted
skirting
skirts
skis
skit
skits
skittish
skulk
skulked
skulking
skulks
skull
skulls
skunk
skunked
skunking
skunks
sky
skyed
skying
skylight
skylights
skyline
skylines
skyrocket
skyrocketed
skyrocketing
skyrockets
skyscraper
skyscrapers
slab
slabbed
slabbing
slabs
slack
slacked
slacken
slackened
slackening
slackens
slacker
slackest
slacking
slacks
slag
slain
slake
slaked
slakes
slaking
slam
slammed
slamming
slams
slander
slandered
slandering
slanders
slang
slant
slanted
slanting
slants
slap
slapped
slapping
slaps
slapstick
slash
slashed
slashes
slashing
slat
slate
slated
slates
slating
slats
slaughter
slaughtered
slaughtering
slaughters
slave
slaved
slavery
slaves
slaving
slavish
slay
slaying
slays
sleazier
sleaziest
sleazy
sled
sledded
sledding
sledgehammer
sleds
sleek
sleeked
sleeker
sleekest
sleeking
sleeks
sleep
sleeper
sleepers
sleepier
sleepiest
sleeping
sleepless
sleeps
sleepy
sleet
sleeted
sleeting
sleets
sleeve
sleeveless
sleeves
sleigh
sleighed
sleighing
sleighs
slender
slenderer
slenderest
slept
slew
slewed
slewing
slews
slice
sliced
slices
slicing
slick
slicked
slicker
slickest
slicking
slicks
slid
slide
slides
sliding
slier
sliest
slight
slighted
slighter
slightest
slighting
slightly
slights
slim
slime
slimier
slimiest
slimmed
slimmer
slimmest
slimming
slims
slimy
sling
slinging
slings
slingshot
slingshots
slink
slinked
slinking
slinks
slip
slipped
slipper
slipperier
slipperiest
slippers
slippery
slipping
slips
slipshod
slit
slither
slithered
slithering
slithers
slits
slitter
slitting
sliver
slivered
slivering
slivers
slob
slobber
slobbered
slobbering
slobbers
slobs
slog
slogan
slogans
slogged
slogging
slogs
slop
slope
sloped
slopes
sloping
slopped
sloppier
sloppiest
slopping
sloppy
slops
slosh
sloshed
sloshes
sloshing
slot
sloth
slothful
sloths
slots
slotted
slotting
slouch
slouched
slouches
slouching
slovenlier
slovenliest
slovenly
slow
slowed
slower
slowest
slowing
slowly
slowness
slows
sludge
slug
slugged
slugging
sluggish
slugs
sluice
sluiced
sluices
sluicing
slum
slumber
slumbered
slumbering
slumbers
slummed
slummer
slumming
slump
slumped
slumping
slumps
slums
slung
slunk
slur
slurred
slurring
slurs
slush
slut
sluts
sly
slyer
slyest
slyness
smack
smacked
smacking
smacks
small
smaller
smallest
smallish
smallpox
smalls
smart
smarted
smarter
smartest
smarting
smartly
smarts
smash
smashed
smashes
smashing
smattering
smatterings
smear
smeared
smearing
smears
smell
smelled
smellier
smelliest
smelling
smells
smelly
smelt
smelted
smelting
smelts
smidge
smidgen
smidgens
smidgeon
smidgeons
smidges
smidgin
smidgins
smile
smiled
smiles
smiling
smirk
smirked
smirking
smirks
smit
smite
smites
smith
smithereens
smiths
smiting
smitten
smock
smocked
smocking
smocks
smog
smoke
smoked
smoker
smokers
smokes
smokestack
smokestacks
smokier
smokiest
smoking
smoky
smolder
smoldered
smoldering
smolders
smooth
smoothed
smoother
smoothes
smoothest
smoothing
smoothly
smoothness
smooths
smote
smother
smothered
smothering
smothers
smoulder
smouldered
smouldering
smoulders
smudge
smudged
smudges
smudging
smug
smugger
smuggest
smuggle
smuggled
smuggler
smugglers
smuggles
smuggling
smugly
smut
smuts
snack
snacked
snacking
snacks
snag
snagged
snagging
snags
snail
snailed
snailing
snails
snake
snaked
snakes
snaking
snap
snapped
snappier
snappiest
snapping
snappy
snaps
snapshot
snapshots
snare
snared
snares
snaring
snarl
snarled
snarling
snarls
snatch
snatched
snatches
snatching
sneak
sneaked
sneaker
sneakers
sneakier
sneakiest
sneaking
sneaks
sneaky
sneer
sneered
sneering
sneers
sneeze
sneezed
sneezes
sneezing
snicker
snickered
snickering
snickers
snide
snider
snidest
sniff
sniffed
sniffing
sniffle
sniffled
sniffles
sniffling
sniffs
snigger
snip
snipe
sniped
sniper
snipers
snipes
sniping
snipped
snippet
snippets
snipping
snips
snitch
snitched
snitches
snitching
snob
snobbery
snobbish
snobs
snooker
snoop
snooped
snooping
snoops
snootier
snootiest
snooty
snooze
snoozed
snoozes
snoozing
snore
snored
snores
snoring
snorkel
snorkeled
snorkeling
snorkelled
snorkelling
snorkels
snort
snorted
snorting
snorts
snot
snots
snout
snouts
snow
snowball
snowballed
snowballing
snowballs
snowdrift
snowdrifts
snowed
snowfall
snowfalls
snowflake
snowflakes
snowier
snowiest
snowing
snowplow
snowplowed
snowplowing
snowplows
snows
snowstorm
snowstorms
snowy
snub
snubbed
snubbing
snubs
snuck
snuff
snuffed
snuffer
snuffing
snuffs
snug
snugged
snugger
snuggest
snugging
snuggle
snuggled
snuggles
snuggling
snugly
snugs
so
soak
soaked
soaking
soaks
soap
soaped
soapier
soapiest
soaping
soaps
soapy
soar
soared
soaring
soars
sob
sobbed
sobbing
sober
sobered
soberer
soberest
sobering
sobers
sobriety
sobs
soccer
sociable
sociables
social
socialism
socialist
socialists
socialize
socialized
socializes
socializing
socially
socials
societies
society
sociological
sociologist
sociologists
sociology
sock
socked
socket
sockets
socking
socks
sod
soda
sodas
sodded
sodden
sodding
sodium
sodomy
sods
sofa
sofas
soft
softball
softballs
soften
softened
softening
softens
softer
softest
softly
softness
software
soggier
soggiest
soggy
soil
soiled
soiling
soils
sojourn
sojourned
sojourning
sojourns
solace
solaced
solaces
solacing
solar
sold
solder
soldered
soldering
solders
soldier
soldiered
soldiering
soldiers
sole
soled
solely
solemn
solemner
solemnest
solemnity
solemnly
soles
soli
solicit
solicited
soliciting
solicitor
solicitors
solicitous
solicits
solid
solidarity
solider
solidest
solidified
solidifies
solidify
solidifying
solidity
solidly
solids
soling
solitaire
solitaires
solitaries
solitary
solitude
solo
soloed
soloing
soloist
soloists
solos
soluble
solubles
solution
solutions
solve
solved
solvent
solvents
solves
solving
somber
sombre
some
somebodies
somebody
someday
somehow
someone
someones
someplace
somersault
somersaulted
somersaulting
somersaults
something
somethings
sometime
sometimes
somewhat
somewhats
somewhere
son
sonata
sonatas
song
songs
sonic
sonnet
sonnets
sonorous
sons
soon
sooner
soonest
soot
soothe
soothed
soothes
soothing
sootier
sootiest
sooty
sop
sophisticate
sophisticated
sophisticates
sophisticating
sophistication
sophistry
sophomore
sophomores
sopped
sopping
soprano
sopranos
sops
sorcerer
sorcerers
sorceress
sorceresses
sorcery
sordid
sore
sorely
sorer
sores
sorest
sororities
sorority
sorrier
sorriest
sorrow
sorrowed
sorrowful
sorrowing
sorrows
sorry
sort
sorta
sorted
sorting
sorts
sought
soul
souls
sound
sounded
sounder
soundest
sounding
soundly
soundproof
soundproofed
soundproofing
soundproofs
sounds
soundtrack
soup
souped
souping
soups
sour
source
sourced
sources
sourcing
soured
sourer
sourest
souring
sours
south
southeast
southeastern
southerlies
southerly
southern
southerner
southerners
southerns
southpaw
southpaws
southward
southwest
southwestern
souvenir
souvenirs
sovereign
sovereigns
sovereignty
sow
sowed
sowing
sown
sows
sox
spa
space
spacecraft
spacecrafts
spaced
spaces
spaceship
spaceships
spacial
spacing
spacious
spade
spaded
spades
spading
spaghetti
span
spangle
spangled
spangles
spangling
spaniel
spaniels
spank
spanked
spanking
spankings
spanks
spanned
spanner
spanners
spanning
spans
spar
spare
spared
sparer
spares
sparest
sparing
spark
sparked
sparking
sparkle
sparkled
sparkler
sparklers
sparkles
sparkling
sparks
sparred
sparring
sparrow
sparrows
spars
sparse
sparsely
sparser
sparsest
spas
spasm
spasmodic
spasms
spat
spate
spatial
spats
spatted
spatter
spattered
spattering
spatters
spatting
spatula
spatulas
spawn
spawned
spawning
spawns
spay
spayed
spaying
spays
speak
speaker
speakers
speaking
speaks
spear
speared
spearhead
spearheaded
spearheading
spearheads
spearing
spearmint
spears
special
specialist
specialists
specialization
specializations
specialize
specialized
specializes
specializing
specially
specials
specialties
specialty
species
specific
specifically
specification
specifications
specifics
specified
specifier
specifies
specify
specifying
specimen
specimens
specious
speck
specked
specking
specks
spectacle
spectacles
spectacular
spectacularly
spectaculars
spectator
spectators
specter
specters
spectra
spectrum
spectrums
speculate
speculated
speculates
speculating
speculation
speculations
speculative
speculator
speculators
sped
speech
speeches
speechless
speed
speedboat
speedboats
speeded
speedier
speediest
speeding
speedometer
speedometers
speeds
speedy
spell
spellbind
spellbinding
spellbinds
spellbound
spelled
speller
spelling
spellings
spells
spelt
spend
spending
spends
spendthrift
spendthrifts
spent
sperm
sperms
spew
spewed
spewing
spews
sphere
spheres
spherical
sphinges
sphinx
sphinxes
spice
spiced
spices
spicier
spiciest
spicing
spicy
spider
spiders
spied
spies
spigot
spigots
spike
spiked
spikes
spiking
spill
spilled
spilling
spills
spilt
spin
spinach
spinal
spinals
spindlier
spindliest
spindly
spine
spineless
spines
spinning
spins
spinster
spinsters
spiral
spiraled
spiraling
spiralled
spiralling
spirals
spire
spires
spirit
spirited
spiriting
spirits
spiritual
spiritually
spirituals
spit
spite
spited
spiteful
spitefuller
spitefullest
spites
spiting
spits
spitted
spitting
spittle
splash
splashed
splashes
splashing
splat
splatter
splattered
splattering
splatters
spleen
spleens
splendid
splendider
splendidest
splendidly
splendor
splice
spliced
splices
splicing
splint
splinted
splinter
splintered
splintering
splinters
splinting
splints
split
splits
splitting
splurge
splurged
splurges
splurging
spoil
spoiled
spoiling
spoils
spoilt
spoke
spoken
spokes
spokesman
spokesmen
spokespeople
spokesperson
spokespersons
spokeswoman
spokeswomen
sponge
sponged
sponges
spongier
spongiest
sponging
spongy
sponsor
sponsored
sponsoring
sponsors
sponsorship
spontaneity
spontaneous
spontaneously
spoof
spoofed
spoofing
spoofs
spook
spooked
spookier
spookiest
spooking
spooks
spooky
spool
spooled
spooling
spools
spoon
spooned
spoonful
spoonfuls
spooning
spoons
spoonsful
sporadic
spore
spores
sporran
sport
sported
sporting
sports
sportsmanship
spot
spotless
spotlight
spotlighted
spotlighting
spotlights
spots
spotted
spottier
spottiest
spotting
spotty
spouse
spouses
spout
spouted
spouting
spouts
sprain
sprained
spraining
sprains
sprang
sprawl
sprawled
sprawling
sprawls
spray
sprayed
spraying
sprays
spread
spreading
spreads
spreadsheet
spreadsheets
spree
spreed
spreeing
sprees
sprier
spriest
sprig
sprigs
spring
springboard
springboards
springier
springiest
springing
springs
springtime
springy
sprinkle
sprinkled
sprinkler
sprinklers
sprinkles
sprinkling
sprinklings
sprint
sprinted
sprinter
sprinters
sprinting
sprints
sprout
sprouted
sprouting
sprouts
spruce
spruced
sprucer
spruces
sprucest
sprucing
sprung
spry
spryer
spryest
spud
spuds
spun
spunk
spur
spurious
spurn
spurned
spurning
spurns
spurred
spurring
spurs
spurt
spurted
spurting
spurts
sputter
sputtered
sputtering
sputters
spy
spying
squabble
squabbled
squabbles
squabbling
squad
squadron
squadrons
squads
squalid
squalider
squalidest
squall
squalled
squalling
squalls
squalor
squander
squandered
squandering
squanders
square
squared
squarely
squarer
squares
squarest
squaring
squash
squashed
squashes
squashing
squat
squats
squatted
squatter
squattest
squatting
squawk
squawked
squawking
squawks
squeak
squeaked
squeakier
squeakiest
squeaking
squeaks
squeaky
squeal
squealed
squealing
squeals
squeamish
squeeze
squeezed
squeezes
squeezing
squelch
squelched
squelches
squelching
squid
squids
squint
squinted
squinter
squintest
squinting
squints
squire
squired
squires
squiring
squirm
squirmed
squirming
squirms
squirrel
squirreled
squirreling
squirrelled
squirrelling
squirrels
squirt
squirted
squirting
squirts
stab
stabbed
stabbing
stability
stabilize
stabilized
stabilizes
stabilizing
stable
stabled
stabler
stables
stablest
stabling
stabs
stack
stacked
stacking
stacks
stadia
stadium
stadiums
staff
staffed
staffing
staffs
stag
stage
stagecoach
stagecoaches
staged
stages
stagger
staggered
staggering
staggers
staging
stagnant
stagnate
stagnated
stagnates
stagnating
stagnation
stags
staid
staider
staidest
stain
stained
staining
stains
stair
staircase
staircases
stairs
stairway
stairways
stake
staked
stakes
staking
stale
staled
stalemate
stalemated
stalemates
stalemating
staler
stales
stalest
staling
stalk
stalked
stalking
stalks
stall
stalled
stalling
stallion
stallions
stalls
stalwart
stalwarts
stamina
stammer
stammered
stammering
stammers
stamp
stamped
stampede
stampeded
stampedes
stampeding
stamping
stamps
stance
stances
stanch
stanched
stancher
stanches
stanchest
stanching
stand
standard
standardization
standardize
standardized
standardizes
standardizing
standards
standby
standbys
standing
standings
standoff
standoffs
standpoint
standpoints
stands
standstill
standstills
stank
stanza
stanzas
staple
stapled
stapler
staplers
staples
stapling
star
starboard
starch
starched
starches
starchier
starchiest
starching
starchy
stardom
stare
stared
stares
starfish
starfishes
staring
stark
starker
starkest
starlight
starred
starrier
starriest
starring
starry
stars
start
started
starter
starters
starting
startle
startled
startles
startling
startlingly
starts
starvation
starve
starved
starves
starving
state
stated
statelier
stateliest
stately
statement
statements
stater
states
statesman
statesmanship
statesmen
static
stating
station
stationary
stationed
stationery
stationing
stations
statistic
statistical
statistically
statistician
statisticians
statistics
statue
statues
stature
statures
status
statuses
statute
statutes
statutory
staunch
staunched
stauncher
staunches
staunchest
staunching
staunchly
stave
staved
staves
staving
stay
stayed
staying
stays
steadfast
steadied
steadier
steadies
steadiest
steadily
steady
steadying
steak
steaks
steal
stealing
steals
stealth
stealthier
stealthiest
stealthily
stealthy
steam
steamed
steamier
steamiest
steaming
steamroller
steamrollered
steamrollering
steamrollers
steams
steamy
steel
steeled
steeling
steels
steep
steeped
steeper
steepest
steeping
steeple
steeples
steeps
steer
steered
steering
steers
stellar
stem
stemmed
stemming
stems
stench
stenches
stencil
stenciled
stenciling
stencilled
stencilling
stencils
stenographer
stenographers
stenography
step
stepladder
stepladders
stepped
stepping
steps
stereo
stereos
stereotype
stereotyped
stereotypes
stereotyping
sterile
sterilization
sterilize
sterilized
sterilizes
sterilizing
sterling
stern
sterner
sternest
sternly
sternness
sterns
stethoscope
stethoscopes
stew
steward
stewarded
stewardess
stewardesses
stewarding
stewards
stewed
stewing
stews
stick
sticker
stickers
stickier
stickies
stickiest
sticking
stickler
sticklers
sticks
sticky
stiff
stiffed
stiffen
stiffened
stiffening
stiffens
stiffer
stiffest
stiffing
stiffly
stiffness
stiffs
stifle
stifled
stifles
stifling
stigma
stigmas
stigmata
still
stillborn
stilled
stiller
stillest
stilling
stillness
stills
stilted
stimulant
stimulants
stimulate
stimulated
stimulates
stimulating
stimulation
stimuli
stimulus
sting
stinger
stingers
stingier
stingiest
stinginess
stinging
stings
stingy
stink
stinking
stinks
stint
stinted
stinting
stints
stipulate
stipulated
stipulates
stipulating
stipulation
stipulations
stir
stirred
stirring
stirrup
stirrups
stirs
stitch
stitched
stitches
stitching
stock
stockade
stockaded
stockades
stockading
stockbroker
stockbrokers
stocked
stockholder
stockholders
stockier
stockiest
stocking
stockings
stockpile
stockpiled
stockpiles
stockpiling
stocks
stocky
stockyard
stockyards
stodgier
stodgiest
stodgy
stoical
stoke
stoked
stokes
stoking
stole
stolen
stoles
stolid
stolider
stolidest
stolidly
stomach
stomached
stomaching
stomachs
stomp
stomped
stomping
stomps
stone
stoned
stones
stoney
stonier
stoniest
stoning
stony
stood
stool
stools
stoop
stooped
stooping
stoops
stop
stopgap
stopgaps
stopover
stopovers
stoppage
stoppages
stopped
stopper
stoppered
stoppering
stoppers
stopping
stops
stopwatch
stopwatches
storage
store
stored
storehouse
storehouses
storekeeper
storekeepers
storeroom
storerooms
stores
storey
storeys
stories
storing
stork
storks
storm
stormed
stormier
stormiest
storming
storms
stormy
story
stout
stouter
stoutest
stove
stoves
stow
stowaway
stowaways
stowed
stowing
stows
straddle
straddled
straddles
straddling
straggle
straggled
straggler
stragglers
straggles
straggling
straight
straighten
straightened
straightening
straightens
straighter
straightest
straightforward
straightforwardly
straightjacket
straightjacketed
straightjacketing
straightjackets
straights
strain
strained
strainer
strainers
straining
strains
strait
straitjacket
straitjacketed
straitjacketing
straitjackets
straits
strand
stranded
stranding
strands
strange
strangely
strangeness
stranger
strangers
strangest
strangle
strangled
strangles
strangling
strangulation
strap
strapped
strapping
straps
strata
stratagem
stratagems
strategic
strategies
strategy
stratified
stratifies
stratify
stratifying
stratosphere
stratospheres
stratum
stratums
straw
strawberries
strawberry
strawed
strawing
straws
stray
strayed
straying
strays
streak
streaked
streaking
streaks
stream
streamed
streamer
streamers
streaming
streamline
streamlined
streamlines
streamlining
streams
street
streetcar
streetcars
streets
strength
strengthen
strengthened
strengthening
strengthens
strengths
strenuous
strenuously
stress
stressed
stresses
stressful
stressing
stretch
stretched
stretcher
stretchers
stretches
stretching
strew
strewed
strewing
strewn
strews
stricken
strict
stricter
strictest
strictly
strictness
stridden
stride
strides
striding
strife
strike
striker
strikers
strikes
striking
strikings
string
stringent
stringier
stringiest
stringing
strings
stringy
strip
stripe
striped
stripes
striping
stripped
stripper
stripping
strips
stript
strive
strived
striven
strives
striving
strode
stroke
stroked
strokes
stroking
stroll
strolled
stroller
strollers
strolling
strolls
strong
stronger
strongest
stronghold
strongholds
strongly
strove
struck
structural
structuralist
structure
structured
structures
structuring
struggle
struggled
struggles
struggling
strum
strummed
strumming
strums
strung
strut
struts
strutted
strutting
stub
stubbed
stubbier
stubbiest
stubbing
stubble
stubborn
stubborner
stubbornest
stubby
stubs
stuck
stud
studded
studding
student
students
studentship
studied
studies
studio
studios
studious
studs
study
studying
stuff
stuffed
stuffier
stuffiest
stuffing
stuffs
stuffy
stumble
stumbled
stumbles
stumbling
stump
stumped
stumping
stumps
stun
stung
stunk
stunned
stunning
stuns
stunt
stunted
stunting
stunts
stupefied
stupefies
stupefy
stupefying
stupendous
stupid
stupider
stupidest
stupidities
stupidity
stupidly
stupids
stupor
stupors
sturdier
sturdiest
sturdy
stutter
stuttered
stuttering
stutters
style
styled
styles
styling
stylish
stylistic
stylus
suave
suaver
suavest
sub
subbed
subbing
subcommittee
subcommittees
subconscious
subconsciously
subdivide
subdivided
subdivides
subdividing
subdivision
subdivisions
subdue
subdued
subdues
subduing
subgroup
subject
subjected
subjecting
subjective
subjects
subjugate
subjugated
subjugates
subjugating
subjunctive
sublet
sublets
subletting
sublime
sublimed
sublimer
sublimes
sublimest
subliming
submarine
submarines
submerge
submerged
submerges
submerging
submersion
submission
submissions
submissive
submit
submits
submitted
submitting
subnormal
subordinate
subordinated
subordinates
subordinating
subprogram
subroutine
subroutines
subs
subscribe
subscribed
subscriber
subscribers
subscribes
subscribing
subscript
subscription
subscriptions
subscripts
subsection
subsections
subsequent
subsequently
subservient
subset
subsets
subside
subsided
subsides
subsidiaries
subsidiary
subsidies
subsiding
subsidize
subsidized
subsidizes
subsidizing
subsidy
subsist
subsisted
subsistence
subsisting
subsists
substance
substances
substandard
substantial
substantially
substantiate
substantiated
substantiates
substantiating
substitute
substituted
substitutes
substituting
substitution
substitutions
subsystem
subterfuge
subterfuges
subterranean
subtle
subtler
subtlest
subtleties
subtlety
subtly
subtract
subtracted
subtracting
subtraction
subtractions
subtracts
suburb
suburban
suburbans
suburbs
subversive
subversives
subvert
subverted
subverting
subverts
subway
subways
succeed
succeeded
succeeding
succeeds
success
successes
successful
successfully
succession
successions
successive
successively
successor
successors
succinct
succincter
succinctest
succinctly
succor
succored
succoring
succors
succulent
succulents
succumb
succumbed
succumbing
succumbs
such
suck
sucked
sucker
suckered
suckering
suckers
sucking
suckle
suckled
suckles
suckling
sucks
suction
suctioned
suctioning
suctions
sudden
suddenly
suds
sue
sued
suede
sues
suffer
suffered
sufferer
sufferers
suffering
sufferings
suffers
suffice
sufficed
suffices
sufficient
sufficiently
sufficing
suffix
suffixed
suffixes
suffixing
suffocate
suffocated
suffocates
suffocating
suffocation
suffrage
sugar
sugared
sugarier
sugariest
sugaring
sugars
sugary
suggest
suggested
suggester
suggesting
suggestion
suggestions
suggestive
suggests
suicidal
suicide
suicides
suing
suit
suitability
suitable
suitably
suitcase
suitcases
suite
suited
suites
suiting
suitor
suitors
suits
sulfur
sulk
sulked
sulkier
sulkies
sulkiest
sulking
sulks
sulky
sullen
sullener
sullenest
sulphur
sultan
sultans
sultrier
sultriest
sultry
sum
summaries
summarily
summarize
summarized
summarizes
summarizing
summary
summed
summer
summered
summering
summers
summing
summit
summits
summon
summoned
summoning
summons
summonsed
summonses
summonsing
sumptuous
sums
sun
sunbathe
sunbathed
sunbathes
sunbathing
sunburn
sunburned
sunburning
sunburns
sunburnt
sundae
sundaes
sundial
sundials
sundown
sundowns
sundries
sundry
sunflower
sunflowers
sung
sunglasses
sunk
sunken
sunlight
sunlit
sunned
sunnier
sunniest
sunning
sunny
sunrise
sunrises
suns
sunscreen
sunscreens
sunset
sunsets
sunshine
suntan
suntanned
suntanning
suntans
sunup
sup
super
superb
superber
superbest
superbly
supercomputer
supercomputers
superficial
superficially
superfluous
superhuman
superimpose
superimposed
superimposes
superimposing
superintendent
superintendents
superior
superiority
superiors
superlative
superlatives
supermarket
supermarkets
supernatural
supernaturals
supers
superscript
superscripts
supersede
superseded
supersedes
superseding
supersonic
superstar
superstars
superstition
superstitions
superstitious
superstructure
superstructures
supervise
supervised
supervises
supervising
supervision
supervisions
supervisor
supervisors
supervisory
supper
suppers
supplant
supplanted
supplanting
supplants
supple
supplement
supplementary
supplemented
supplementing
supplements
suppler
supplest
supplied
supplier
suppliers
supplies
supply
supplying
support
supported
supporter
supporters
supporting
supportive
supports
suppose
supposed
supposedly
supposes
supposing
supposition
suppositions
suppress
suppressed
suppresses
suppressing
suppression
supremacy
supreme
supremely
surcharge
surcharged
surcharges
surcharging
sure
surely
surer
surest
surf
surface
surfaced
surfaces
surfacing
surfboard
surfboarded
surfboarding
surfboards
surfed
surfing
surfs
surge
surged
surgeon
surgeons
surgeries
surgery
surges
surgical
surging
surlier
surliest
surly
surmise
surmised
surmises
surmising
surmount
surmounted
surmounting
surmounts
surname
surnames
surpass
surpassed
surpasses
surpassing
surplus
surplused
surpluses
surplusing
surplussed
surplussing
surprise
surprised
surprises
surprising
surprisingly
surreal
surrender
surrendered
surrendering
surrenders
surreptitious
surround
surrounded
surrounding
surroundings
surrounds
surveillance
survey
surveyed
surveying
surveyor
surveyors
surveys
survival
survivals
survive
survived
survives
surviving
survivor
survivors
susceptible
suspect
suspected
suspecting
suspects
suspend
suspended
suspender
suspenders
suspending
suspends
suspense
suspension
suspensions
suspicion
suspicions
suspicious
suspiciously
sustain
sustainable
sustained
sustaining
sustains
sustenance
swab
swabbed
swabbing
swabs
swagger
swaggered
swaggerer
swaggering
swaggers
swallow
swallowed
swallowing
swallows
swam
swamp
swamped
swampier
swampiest
swamping
swamps
swampy
swan
swans
swap
swapped
swapping
swaps
swarm
swarmed
swarming
swarms
swarthier
swarthiest
swarthy
swat
swathe
swathed
swathes
swathing
swats
swatted
swatting
sway
swayed
swaying
sways
swear
swearing
swears
sweat
sweater
sweaters
sweating
sweats
sweaty
sweep
sweeper
sweepers
sweeping
sweepings
sweeps
sweepstake
sweepstakes
sweet
sweeten
sweetened
sweetening
sweetens
sweeter
sweetest
sweetheart
sweethearts
sweetly
sweetness
sweets
swell
swelled
sweller
swellest
swelling
swellings
swells
swept
swerve
swerved
swerves
swerving
swift
swifter
swiftest
swiftly
swifts
swig
swigged
swigging
swigs
swill
swilled
swilling
swills
swim
swimming
swims
swindle
swindled
swindler
swindlers
swindles
swindling
swine
swines
swing
swinging
swings
swipe
swiped
swipes
swiping
swirl
swirled
swirling
swirls
swish
swished
swisher
swishes
swishest
swishing
switch
switchable
switchboard
switchboards
switched
switcher
switches
switching
swivel
swiveled
swiveling
swivelled
swivelling
swivels
swollen
swoon
swooned
swooning
swoons
swoop
swooped
swooping
swoops
sword
swordfish
swordfishes
swords
swore
sworn
swum
swung
syllabi
syllable
syllables
syllabus
syllabuses
symbol
symbolic
symbolism
symbolize
symbolized
symbolizes
symbolizing
symbols
symmetric
symmetrical
symmetry
sympathetic
sympathetically
sympathies
sympathize
sympathized
sympathizes
sympathizing
sympathy
symphonic
symphonies
symphony
symptom
symptomatic
symptoms
synagog
synagogs
synagogue
synagogues
synapse
synapses
synchronization
synchronize
synchronized
synchronizes
synchronizing
synchronous
syndicate
syndicated
syndicates
syndicating
syndrome
syndromes
synonym
synonymous
synonyms
synopses
synopsis
syntactic
syntactically
syntax
syntheses
synthesis
synthesize
synthesized
synthesizer
synthesizers
synthesizes
synthesizing
synthetic
synthetics
syphilis
syphon
syphoned
syphoning
syphons
syringe
syringed
syringes
syringing
syrup
syrups
system
systematic
systematically
systems
tab
tabbed
tabbies
tabbing
tabby
tabernacle
tabernacles
table
tablecloth
tablecloths
tabled
tables
tablespoon
tablespoonful
tablespoonfuls
tablespoons
tablespoonsful
tablet
tablets
tabling
tabloid
tabloids
taboo
tabooed
tabooing
taboos
tabs
tabu
tabued
tabuing
tabulate
tabulated
tabulates
tabulating
tabulation
tabus
tacit
tacitly
taciturn
tack
tacked
tackier
tackiest
tacking
tackle
tackled
tackles
tackling
tacks
tacky
taco
tacos
tact
tactful
tactfully
tactic
tactical
tactics
tactless
tactlessly
tadpole
tadpoles
tag
tagged
tagging
tags
tail
tailed
tailgate
tailgated
tailgates
tailgating
tailing
taillight
taillights
tailor
tailored
tailoring
tailors
tails
tailspin
tailspins
taint
tainted
tainting
taints
take
taken
takeoff
takeoffs
takeover
taker
takers
takes
taking
talc
tale
talent
talented
talents
tales
talisman
talismans
talk
talkative
talked
talker
talkers
talking
talks
tall
taller
tallest
tallied
tallies
tallow
tally
tallying
talon
talons
tambourine
tambourines
tame
tamed
tamely
tameness
tamer
tames
tamest
taming
tamper
tampered
tampering
tampers
tan
tandem
tandems
tang
tangent
tangential
tangents
tangerine
tangerines
tangible
tangibles
tangle
tangled
tangles
tangling
tango
tangoed
tangoing
tangos
tangs
tank
tankard
tankards
tanked
tanker
tankers
tanking
tanks
tanned
tanner
tannest
tanning
tans
tantalize
tantalized
tantalizes
tantalizing
tantamount
tantrum
tantrums
tap
tape
taped
taper
tapered
tapering
tapers
tapes
tapestries
tapestry
taping
tapped
tapping
taps
tar
tarantula
tarantulae
tarantulas
tardier
tardiest
tardiness
tardy
target
targeted
targeting
targets
tariff
tariffs
tarnish
tarnished
tarnishes
tarnishing
tarpaulin
tarpaulins
tarred
tarried
tarrier
tarries
tarriest
tarring
tarry
tarrying
tars
tart
tartan
tartans
tartar
tartars
tarter
tartest
tarts
task
tasked
tasking
tasks
tassel
tasseled
tasseling
tasselled
tasselling
tassels
taste
tasted
tasteful
tastefully
tasteless
tastes
tastier
tastiest
tasting
tasty
tattle
tattled
tattles
tattling
tattoo
tattooed
tattooing
tattoos
tatty
taught
taunt
taunted
taunting
taunts
taut
tauter
tautest
tautology
tavern
taverns
tawdrier
tawdriest
tawdry
tawnier
tawniest
tawny
tax
taxable
taxation
taxed
taxes
taxi
taxicab
taxicabs
taxied
taxies
taxiing
taxing
taxis
taxpayer
taxpayers
taxying
tea
teach
teacher
teachers
teaches
teaching
teachings
teacup
teacups
teak
teaks
team
teamed
teaming
teammate
teammates
teams
teamster
teamsters
teamwork
teapot
teapots
tear
teardrop
teardrops
teared
tearful
tearing
tears
teas
tease
teased
teases
teasing
teaspoon
teaspoons
teat
teats
technical
technicalities
technicality
technically
technician
technicians
technique
techniques
technological
technologically
technologies
technology
tedious
tediously
tedium
tee
teed
teeing
teem
teemed
teeming
teems
teen
teenage
teenager
teenagers
teens
teepee
teepees
tees
teeter
teetered
teetering
teeters
teeth
teethe
teethed
teethes
teething
teetotal
teetotaler
teetotalers
teetotaller
teetotallers
telecommunications
telegram
telegrams
telegraph
telegraphed
telegraphing
telegraphs
telepathic
telepathy
telephone
telephoned
telephones
telephoning
telescope
telescoped
telescopes
telescoping
teletype
televise
televised
televises
televising
television
televisions
tell
teller
tellers
telling
tells
telltale
telltales
temper
temperament
temperamental
temperaments
temperance
temperate
temperature
temperatures
tempered
tempering
tempers
tempest
tempests
tempestuous
tempi
template
temple
temples
tempo
temporal
temporaries
temporarily
temporary
tempos
tempt
temptation
temptations
tempted
tempting
tempts
ten
tenable
tenacious
tenacity
tenancies
tenancy
tenant
tenanted
tenanting
tenants
tend
tended
tendencies
tendency
tender
tendered
tenderer
tenderest
tendering
tenderize
tenderized
tenderizes
tenderizing
tenderly
tenderness
tenders
tending
tendon
tendons
tendril
tendrils
tends
tenement
tenements
tenet
tenets
tennis
tenor
tenors
tens
tense
tensed
tenser
tenses
tensest
tensing
tension
tensions
tensors
tent
tentacle
tentacles
tentative
tentatively
tented
tenth
tenths
tenting
tents
tenuous
tenure
tenured
tenures
tenuring
tepee
tepees
tepid
term
termed
terminal
terminally
terminals
terminate
terminated
terminates
terminating
termination
terminator
terminators
terming
termini
terminologies
terminology
terminus
terminuses
termite
termites
termly
terms
terrace
terraced
terraces
terracing
terrain
terrains
terrestrial
terrestrials
terrible
terribly
terrier
terriers
terrific
terrified
terrifies
terrify
terrifying
territorial
territorials
territories
territory
terror
terrorism
terrorist
terrorists
terrorize
terrorized
terrorizes
terrorizing
terrors
terse
tersely
terseness
terser
tersest
test
testable
testament
testaments
tested
tester
testers
testes
testicle
testicles
testified
testifies
testify
testifying
testimonial
testimonials
testimonies
testimony
testing
testis
tests
tetanus
tether
tethered
tethering
tethers
text
textbook
textbooks
textile
textiles
texts
textual
textually
texture
textured
textures
texturing
than
thank
thanked
thankful
thankfully
thanking
thankless
thanks
that
thatch
thatched
thatcher
thatches
thatching
thaw
thawed
thawing
thaws
the
theater
theaters
theatre
theatres
theatrical
thee
theft
thefts
their
theirs
theist
theists
them
theme
themes
themselves
then
thence
theologian
theologians
theological
theologies
theology
theorem
theorems
theoretic
theoretical
theoretically
theories
theorist
theorists
theorize
theorized
theorizes
theorizing
theory
therapeutic
therapies
therapist
therapists
therapy
there
thereabouts
thereafter
thereby
therefore
therein
thereof
thereon
thereupon
thermal
thermals
thermodynamics
thermometer
thermometers
thermostat
thermostats
thesauri
thesaurus
thesauruses
these
theses
thesis
theta
they
thick
thicken
thickened
thickening
thickens
thicker
thickest
thicket
thickets
thickly
thickness
thicknesses
thief
thieve
thieves
thigh
thighs
thimble
thimbles
thin
thing
things
think
thinker
thinkers
thinking
thinks
thinly
thinned
thinner
thinnest
thinning
thins
third
thirds
thirst
thirsted
thirstier
thirstiest
thirsting
thirsts
thirsty
thirteen
thirteens
thirteenth
thirteenths
thirties
thirtieth
thirtieths
thirty
this
thistle
thistles
thong
thongs
thorn
thornier
thorniest
thorns
thorny
thorough
thoroughbred
thoroughbreds
thorougher
thoroughest
thoroughfare
thoroughfares
thoroughly
those
thou
though
thought
thoughtful
thoughtfully
thoughtfulness
thoughtless
thoughtlessly
thoughts
thous
thousand
thousands
thousandth
thousandths
thrash
thrashed
thrashes
thrashing
thread
threadbare
threaded
threading
threads
threat
threaten
threatened
threatening
threatens
threats
three
threes
thresh
threshed
thresher
threshers
threshes
threshing
threshold
thresholds
threw
thrice
thrift
thriftier
thriftiest
thrifts
thrifty
thrill
thrilled
thriller
thrillers
thrilling
thrills
thrive
thrived
thriven
thrives
thriving
throat
throats
throb
throbbed
throbbing
throbs
throne
thrones
throng
thronged
thronging
throngs
throttle
throttled
throttles
throttling
through
throughout
throughput
throve
throw
throwaway
throwback
throwbacks
throwing
thrown
throws
thru
thrust
thrusting
thrusts
thud
thudded
thudding
thuds
thug
thugs
thumb
thumbed
thumbing
thumbs
thumbtack
thumbtacks
thump
thumped
thumping
thumps
thunder
thunderbolt
thunderbolts
thundered
thundering
thunderous
thunders
thunderstorm
thunderstorms
thunderstruck
thus
thwart
thwarted
thwarting
thwarts
thy
thyme
thyroid
thyroids
tiara
tiaras
tick
ticked
ticket
ticketed
ticketing
tickets
ticking
tickle
tickled
tickles
tickling
ticklish
ticks
tidal
tidbit
tidbits
tide
tided
tides
tidied
tidier
tidies
tidiest
tiding
tidy
tidying
tie
tied
tieing
tier
tiers
ties
tiff
tiffed
tiffing
tiffs
tiger
tigers
tight
tighten
tightened
tightening
tightens
tighter
tightest
tightly
tightness
tightrope
tightropes
tights
tightwad
tightwads
tilde
tile
tiled
tiles
tiling
till
tilled
tilling
tills
tilt
tilted
tilting
tilts
timber
timbered
timbering
timbers
time
timed
timekeeper
timekeepers
timeless
timelier
timeliest
timely
timer
timers
times
timescale
timescales
timetable
timetables
timezone
timid
timider
timidest
timidity
timidly
timing
timings
tin
tinder
ting
tinge
tinged
tingeing
tinges
tinging
tingle
tingled
tingles
tingling
tings
tinier
tiniest
tinker
tinkered
tinkering
tinkers
tinkle
tinkled
tinkles
tinkling
tinned
tinnier
tinniest
tinning
tinny
tins
tinsel
tinseled
tinseling
tinselled
tinselling
tinsels
tint
tinted
tinting
tints
tiny
tip
tipi
tipis
tipped
tipping
tips
tipsier
tipsiest
tipsy
tiptoe
tiptoed
tiptoeing
tiptoes
tirade
tirades
tire
tired
tireder
tiredest
tireless
tires
tiresome
tiring
tissue
tissues
tit
titbit
titbits
titillate
titillated
titillates
titillating
title
titled
titles
titling
tits
titter
tittered
tittering
titters
to
toad
toads
toadstool
toadstools
toast
toasted
toaster
toasters
toasting
toasts
tobacco
tobaccoes
tobaccos
toboggan
tobogganed
tobogganing
toboggans
today
toddle
toddled
toddler
toddlers
toddles
toddling
toe
toed
toeing
toenail
toenails
toes
toffee
toffees
toffies
toffy
toga
togae
togas
together
toggle
toil
toiled
toilet
toileted
toileting
toilets
toiling
toils
token
tokens
told
tolerable
tolerably
tolerance
tolerances
tolerant
tolerate
tolerated
tolerates
tolerating
toll
tolled
tolling
tolls
tomahawk
tomahawked
tomahawking
tomahawks
tomato
tomatoes
tomb
tombed
tombing
tomboy
tomboys
tombs
tombstone
tombstones
tomcat
tomcats
tome
tomes
tomorrow
tomorrows
ton
tonal
tone
toned
tones
tong
tongs
tongue
tongued
tongues
tonguing
tonic
tonics
tonight
toning
tonnage
tonnages
tonne
tonnes
tons
tonsil
tonsillitis
tonsils
too
took
tool
tooled
tooling
toolkit
tools
toot
tooted
tooth
toothache
toothaches
toothbrush
toothbrushes
toothpaste
toothpastes
toothpick
toothpicks
tooting
toots
top
topaz
topazes
topic
topical
topics
topographies
topography
topology
topped
topping
topple
toppled
topples
toppling
tops
torch
torched
torches
torching
tore
torment
tormented
tormenter
tormenters
tormenting
tormentor
tormentors
torments
torn
tornado
tornadoes
tornados
torpedo
torpedoed
torpedoes
torpedoing
torpedos
torque
torrent
torrential
torrents
torrid
torrider
torridest
torsi
torso
torsos
tortilla
tortillas
tortoise
tortoises
tortuous
torture
tortured
tortures
torturing
toss
tossed
tosses
tossing
tost
tot
total
totaled
totaling
totalitarian
totalitarianism
totalitarians
totalities
totality
totalled
totalling
totally
totals
tote
toted
totem
totems
totes
toting
tots
totted
totter
tottered
tottering
totters
totting
toucan
toucans
touch
touchdown
touchdowns
touched
touches
touchier
touchiest
touching
touchings
touchy
tough
toughen
toughened
toughening
toughens
tougher
toughest
toughness
toughs
toupee
toupees
tour
toured
touring
tourist
tourists
tournament
tournaments
tourniquet
tourniquets
tours
tousle
tousled
tousles
tousling
tout
touted
touting
touts
tow
toward
towards
towed
towel
toweled
toweling
towelled
towelling
towellings
towels
tower
towered
towering
towers
towing
town
towns
townspeople
tows
toxic
toxin
toxins
toy
toyed
toying
toys
trace
traced
traces
tracing
track
tracked
tracking
tracks
tract
traction
tractor
tractors
tracts
trade
traded
trademark
trademarked
trademarking
trademarks
trader
traders
trades
trading
tradition
traditional
traditionalist
traditionally
traditions
traffic
trafficked
trafficking
traffics
tragedies
tragedy
tragic
tragically
trail
trailed
trailer
trailers
trailing
trails
train
trained
trainee
trainees
trainer
trainers
training
trains
trait
traitor
traitorous
traitors
traits
tramp
tramped
tramping
trample
trampled
tramples
trampling
trampoline
trampolines
tramps
trance
trances
tranquil
tranquiler
tranquilest
tranquility
tranquilize
tranquilized
tranquilizer
tranquilizers
tranquilizes
tranquilizing
tranquiller
tranquillest
tranquillity
tranquillize
tranquillized
tranquillizer
tranquillizers
tranquillizes
tranquillizing
transact
transacted
transacting
transaction
transactions
transacts
transatlantic
transcend
transcended
transcending
transcends
transcontinental
transcribe
transcribed
transcribes
transcribing
transcript
transcription
transcriptions
transcripts
transfer
transferable
transferred
transferring
transfers
transform
transformation
transformations
transformed
transformer
transformers
transforming
transforms
transfusion
transfusions
transgress
transgressed
transgresses
transgressing
transgression
transgressions
transient
transients
transistor
transistors
transit
transited
transiting
transition
transitional
transitioned
transitioning
transitions
transitive
transitives
transitory
transits
transitted
transitting
translate
translated
translates
translating
translation
translations
translator
translators
transliteration
translucent
transmission
transmissions
transmit
transmits
transmitted
transmitter
transmitters
transmitting
transparencies
transparency
transparent
transparently
transpire
transpired
transpires
transpiring
transplant
transplanted
transplanting
transplants
transport
transportable
transportation
transported
transporting
transports
transpose
transposed
transposes
transposing
transverse
transverses
trap
trapdoor
trapeze
trapezes
trapezoid
trapezoids
trapped
trapper
trappers
trapping
trappings
traps
trash
trashcan
trashed
trashes
trashier
trashiest
trashing
trashy
trauma
traumas
traumata
traumatic
traumatize
traumatized
traumatizes
traumatizing
travel
traveled
traveler
travelers
traveling
travelings
travelled
traveller
travellers
travelling
travels
traverse
traversed
traverses
traversing
travestied
travesties
travesty
travestying
trawl
trawled
trawler
trawlers
trawling
trawls
tray
trays
treacheries
treacherous
treachery
treacle
tread
treading
treadmill
treadmills
treads
treason
treasure
treasured
treasurer
treasurers
treasures
treasuries
treasuring
treasury
treat
treated
treaties
treating
treatise
treatises
treatment
treatments
treats
treaty
treble
trebled
trebles
trebling
tree
treed
treeing
trees
trek
trekked
trekking
treks
trellis
trellised
trellises
trellising
tremble
trembled
trembles
trembling
tremendous
tremendously
tremor
tremors
trench
trenched
trenches
trenching
trend
trended
trendier
trendies
trendiest
trending
trends
trendy
trepidation
trespass
trespassed
trespasser
trespassers
trespasses
trespassing
trestle
trestles
trial
trialed
trialing
trials
triangle
triangles
triangular
tribal
tribe
tribes
tribulation
tribulations
tribunal
tribunals
tributaries
tributary
tribute
tributes
trick
tricked
trickery
trickier
trickiest
tricking
trickle
trickled
trickles
trickling
tricks
trickster
tricksters
tricky
tricycle
tricycles
tried
tries
trifle
trifled
trifles
trifling
trigger
triggered
triggering
triggers
trigonometry
trill
trilled
trilling
trillion
trillions
trills
trilogies
trilogy
trim
trimester
trimesters
trimmed
trimmer
trimmest
trimming
trims
trinity
trinket
trinkets
trio
trios
trip
tripe
triple
tripled
triples
triplet
triplets
triplicate
triplicated
triplicates
triplicating
tripling
tripod
tripods
tripos
tripped
tripping
trips
trite
triter
tritest
triumph
triumphant
triumphed
triumphing
triumphs
trivia
trivial
triviality
trivially
trod
trodden
troll
trolled
trolley
trolleys
trollies
trolling
trolls
trolly
trombone
trombones
troop
trooped
trooper
troopers
trooping
troops
trophies
trophy
tropical
trot
trots
trotted
trotting
trouble
troubled
troublemaker
troublemakers
troubles
troublesome
troubling
trough
troughs
trounce
trounced
trounces
trouncing
troupe
trouped
troupes
trouping
trouser
trousers
trout
trouts
trowel
troweled
troweling
trowelled
trowelling
trowels
truancy
truant
truanted
truanting
truants
truce
truces
truck
trucked
trucking
trucks
trudge
trudged
trudges
trudging
true
trued
trueing
truer
trues
truest
truffle
truffles
truing
truism
truisms
truly
trump
trumped
trumpet
trumpeted
trumpeting
trumpets
trumping
trumps
truncate
truncated
truncates
truncating
truncation
trunk
trunking
trunks
trust
trusted
trustee
trustees
trustful
trustier
trusties
trustiest
trusting
trusts
trustworthier
trustworthiest
trustworthy
trusty
truth
truthful
truthfully
truthfulness
truths
try
trying
tryout
tryouts
tsar
tsars
tub
tuba
tubas
tube
tubed
tuberculosis
tubes
tubing
tubs
tubular
tuck
tucked
tucking
tucks
tuft
tufted
tufting
tufts
tug
tugged
tugging
tugs
tuition
tulip
tulips
tumble
tumbled
tumbler
tumblers
tumbles
tumbling
tummies
tummy
tumor
tumors
tumult
tumults
tumultuous
tuna
tunas
tundra
tundras
tune
tuned
tuneful
tuner
tuners
tunes
tunic
tunics
tuning
tunnel
tunneled
tunneling
tunnelings
tunnelled
tunnelling
tunnels
turban
turbans
turbine
turbines
turbulence
turbulent
tureen
tureens
turf
turfed
turfing
turfs
turgid
turkey
turkeys
turmoil
turmoils
turn
turnaround
turned
turner
turning
turnip
turnips
turnout
turnouts
turnover
turnovers
turnpike
turnpikes
turns
turnstile
turnstiles
turntable
turntables
turpentine
turquoise
turquoises
turret
turrets
turtle
turtleneck
turtlenecks
turtles
turves
tusk
tusks
tussle
tussled
tussles
tussling
tutor
tutored
tutorial
tutorials
tutoring
tutors
tuxedo
tuxedoes
tuxedos
twang
twanged
twanging
twangs
tweak
tweaked
tweaking
tweaks
twee
tweed
tweet
tweeted
tweeting
tweets
tweezers
twelfth
twelfths
twelve
twelves
twenties
twentieth
twentieths
twenty
twice
twiddle
twiddled
twiddles
twiddling
twig
twigged
twigging
twigs
twilight
twin
twine
twined
twines
twinge
twinged
twingeing
twinges
twinging
twining
twinkle
twinkled
twinkles
twinkling
twinned
twinning
twins
twirl
twirled
twirling
twirls
twist
twisted
twister
twisters
twisting
twists
twitch
twitched
twitches
twitching
twitter
twittered
twittering
twitters
two
twos
tycoon
tycoons
tying
type
typed
typeface
types
typescript
typeset
typesets
typesetter
typesetting
typewriter
typewriters
typhoid
typhoon
typhoons
typhus
typical
typically
typified
typifies
typify
typifying
typing
typist
typists
typographic
typographical
tyrannical
tyrannies
tyrannize
tyrannized
tyrannizes
tyrannizing
tyranny
tyrant
tyrants
tzar
tzars
ubiquitous
udder
udders
ugh
uglier
ugliest
ugliness
ugly
ulcer
ulcers
ulterior
ultimata
ultimate
ultimately
ultimatum
ultimatums
ultra
ultrasonic
ultraviolet
umbrella
umbrellas
umpire
umpired
umpires
umpiring
umpteen
unable
unacceptable
unacceptably
unaccepted
unaccountable
unaccountably
unadulterated
unaffected
unaltered
unambiguous
unambiguously
unanimity
unanimous
unanimously
unanswerable
unanswered
unarmed
unassigned
unassuming
unattached
unattainable
unattended
unattractive
unauthorized
unavailable
unavoidable
unaware
unawares
unbalanced
unbearable
unbearably
unbeatable
unbecoming
unbelievable
unbelievably
unbeliever
unbelievers
unbiased
unbiassed
unblock
unblocked
unblocking
unblocks
unborn
unbreakable
unbroken
unburden
unburdened
unburdening
unburdens
uncannier
uncanniest
uncanny
unceasing
uncertain
uncertainties
uncertainty
unchallenged
unchanged
uncharitable
unchristian
uncle
unclean
uncleaner
uncleanest
unclear
uncles
uncomfortable
uncomfortably
uncommon
uncommoner
uncommonest
uncompromising
unconcerned
unconditional
unconditionally
unconfirmed
unconnected
unconscious
unconsciously
unconstitutional
uncontrollable
uncontrolled
uncontroversial
unconventional
unconvinced
unconvincing
uncountable
uncouth
uncover
uncovered
uncovering
uncovers
uncultured
uncut
undamaged
undaunted
undecidable
undecided
undecideds
undefined
undemocratic
undeniable
undeniably
under
underbrush
undercover
undercurrent
undercurrents
undercut
undercuts
undercutting
underdog
underdogs
underestimate
underestimated
underestimates
underestimating
underflow
underfoot
undergarment
undergarments
undergo
undergoes
undergoing
undergone
undergraduate
undergraduates
underground
undergrounds
undergrowth
underhanded
underlain
underlay
underlays
underlie
underlies
underline
underlined
underlines
underlining
underlying
undermine
undermined
undermines
undermining
underneath
underneaths
undernourished
underpants
underpass
underpasses
underprivileged
underrate
underrated
underrates
underrating
underscore
underscored
underscores
underscoring
undershirt
undershirts
underside
undersides
understand
understandable
understandably
understanding
understandings
understands
understate
understated
understatement
understatements
understates
understating
understood
understudied
understudies
understudy
understudying
undertake
undertaken
undertaker
undertakers
undertakes
undertaking
undertakings
undertone
undertones
undertook
undertow
undertows
underwater
underwear
underweight
underwent
underworld
underworlds
underwrite
underwrites
underwriting
underwritten
underwrote
undeserved
undesirable
undesirables
undetected
undeveloped
undid
undisturbed
undo
undocumented
undoes
undoing
undoings
undone
undoubted
undoubtedly
undress
undressed
undresses
undressing
undue
unduly
undying
unearth
unearthed
unearthing
unearthly
unearths
uneasier
uneasiest
uneasily
uneasiness
uneasy
uneconomic
uneconomical
uneducated
unemployable
unemployed
unemployment
unenlightened
unequal
unequaled
unequalled
unequivocal
unerring
unethical
uneven
unevener
unevenest
unevenly
uneventful
unexpected
unexpectedly
unexplained
unfailing
unfair
unfairer
unfairest
unfairly
unfaithful
unfamiliar
unfasten
unfastened
unfastening
unfastens
unfavorable
unfeasible
unfeeling
unfilled
unfinished
unfit
unfits
unfitted
unfitting
unfold
unfolded
unfolding
unfolds
unforeseen
unforgettable
unforgivable
unfortunate
unfortunately
unfortunates
unfounded
unfriendlier
unfriendliest
unfriendly
unfunny
unfurl
unfurled
unfurling
unfurls
ungainlier
ungainliest
ungainly
ungodlier
ungodliest
ungodly
ungrammatical
ungrateful
unhappier
unhappiest
unhappily
unhappiness
unhappy
unhealthier
unhealthiest
unhealthy
unheard
unhelpful
unhook
unhooked
unhooking
unhooks
unicorn
unicorns
unicycle
unidentified
unification
unified
unifies
uniform
uniformed
uniforming
uniformity
uniformly
uniforms
unify
unifying
unilateral
unilaterally
unimaginative
unimportant
unimpressed
uninformative
uninformed
uninhibited
uninitiated
uninspired
uninspiring
unintelligent
unintelligible
unintended
unintentional
unintentionally
uninterested
uninteresting
union
unionize
unionized
unionizes
unionizing
unions
unique
uniquely
uniqueness
uniquer
uniquest
unison
unit
unite
united
unites
unities
uniting
units
unity
universal
universally
universals
universe
universes
universities
university
unjust
unjustifiable
unjustified
unjustly
unkempt
unkind
unkinder
unkindest
unkindlier
unkindliest
unkindly
unknown
unknowns
unlabeled
unlawful
unleash
unleashed
unleashes
unleashing
unless
unlike
unlikelier
unlikeliest
unlikely
unlimited
unload
unloaded
unloading
unloads
unlock
unlocked
unlocking
unlocks
unluckier
unluckiest
unlucky
unman
unmanned
unmanning
unmans
unmarked
unmarried
unmask
unmasked
unmasking
unmasks
unmistakable
unmistakably
unmitigated
unmodified
unmoved
unnamed
unnatural
unnecessarily
unnecessary
unnerve
unnerved
unnerves
unnerving
unnoticed
unobtainable
unoccupied
unofficial
unoriginal
unorthodox
unpack
unpacked
unpacking
unpacks
unpaid
unparalleled
unpick
unpleasant
unpleasantly
unpleasantness
unpopular
unpopularity
unprecedented
unpredictable
unprepared
unprincipled
unprintable
unprivileged
unprotected
unproven
unprovoked
unpublished
unqualified
unquestionable
unquestionably
unravel
unraveled
unraveling
unravelled
unravelling
unravels
unread
unreadable
unreal
unrealistic
unreasonable
unreasonably
unrecognized
unrelated
unrelenting
unreliability
unreliable
unremarkable
unrepeatable
unrepresentative
unreservedly
unresolved
unrest
unrestricted
unrivaled
unrivalled
unruffled
unrulier
unruliest
unruly
unsafe
unsafer
unsafest
unsaid
unsanitary
unsatisfactory
unsatisfied
unsavory
unsay
unsaying
unsays
unscathed
unscheduled
unscientific
unscrew
unscrewed
unscrewing
unscrews
unscrupulous
unseasonable
unseat
unseated
unseating
unseats
unseemlier
unseemliest
unseemly
unseen
unset
unsettle
unsettled
unsettles
unsettling
unsightlier
unsightliest
unsightly
unsigned
unskilled
unsolicited
unsolved
unsophisticated
unsound
unsounder
unsoundest
unspeakable
unspecified
unstable
unstabler
unstablest
unstructured
unstuck
unsubstantiated
unsuccessful
unsuccessfully
unsuitable
unsuited
unsung
unsupportable
unsupported
unsure
unsuspecting
untangle
untangled
untangles
untangling
untenable
unthinkable
untidier
untidiest
untidy
untie
untied
unties
until
untiring
unto
untold
untouched
untrained
untrue
untruer
untruest
untrustworthy
untying
unusable
unused
unusual
unusually
unveil
unveiled
unveiling
unveils
unwanted
unwarranted
unwary
unwashed
unwelcome
unwell
unwieldier
unwieldiest
unwieldy
unwilling
unwillingness
unwind
unwinding
unwinds
unwise
unwiser
unwisest
unwittingly
unworkable
unworthy
unwound
unwrap
unwrapped
unwrapping
unwraps
unwritten
up
upbeat
upbeats
upbringing
upbringings
update
updated
updates
updating
upend
upended
upending
upends
upgrade
upgraded
upgrades
upgrading
upheaval
upheavals
upheld
uphill
uphills
uphold
upholding
upholds
upholster
upholstered
upholsterer
upholsterers
upholstering
upholsters
upholstery
upkeep
uplift
uplifted
uplifting
uplifts
upload
upon
upped
upper
uppermost
uppers
upping
upright
uprights
uprising
uprisings
uproar
uproars
uproot
uprooted
uprooting
uproots
ups
upset
upsets
upsetting
upshot
upshots
upside
upstairs
upstanding
upstart
upstarted
upstarting
upstarts
upstream
uptake
uptight
uptown
upturn
upturned
upturning
upturns
upward
upwardly
upwards
uranium
urban
urbane
urbaner
urbanest
urchin
urchins
urge
urged
urgency
urgent
urgently
urges
urging
urinate
urinated
urinates
urinating
urine
urn
urns
us
usable
usage
usages
use
useable
used
useful
usefully
usefulness
useless
uselessly
uselessness
user
users
uses
usher
ushered
ushering
ushers
using
usual
usually
usurp
usurped
usurping
usurps
utensil
utensils
uteri
uterus
uteruses
utilitarian
utilitarianism
utilities
utility
utilization
utilize
utilized
utilizes
utilizing
utmost
utter
utterance
utterances
uttered
uttering
utterly
utters
vacancies
vacancy
vacant
vacate
vacated
vacates
vacating
vacation
vacationed
vacationing
vacations
vaccinate
vaccinated
vaccinates
vaccinating
vaccination
vaccinations
vaccine
vaccines
vacillate
vacillated
vacillates
vacillating
vacua
vacuous
vacuum
vacuumed
vacuuming
vacuums
vagabond
vagabonded
vagabonding
vagabonds
vagaries
vagary
vagina
vaginae
vaginal
vaginas
vagrant
vagrants
vague
vaguely
vagueness
vaguer
vaguest
vain
vainer
vainest
valentine
valentines
valet
valeted
valeting
valets
valiant
valid
validate
validated
validates
validating
validation
validity
validly
valise
valises
valley
valleys
valor
valuable
valuables
value
valued
valueless
values
valuing
valve
valved
valves
valving
vampire
vampires
van
vandal
vandalism
vandalize
vandalized
vandalizes
vandalizing
vandals
vane
vanes
vanguard
vanguards
vanilla
vanillas
vanish
vanished
vanishes
vanishing
vanities
vanity
vanned
vanning
vanquish
vanquished
vanquishes
vanquishing
vans
vapor
vaporize
vaporized
vaporizes
vaporizing
vapors
variable
variables
variance
variant
variants
variation
variations
varied
varies
varieties
variety
various
variously
varnish
varnished
varnishes
varnishing
varsities
varsity
vary
varying
vase
vases
vast
vaster
vastest
vastly
vastness
vasts
vat
vats
vatted
vatting
vault
vaulted
vaulting
vaults
veal
vector
vectors
veer
veered
veering
veers
vegetable
vegetables
vegetarian
vegetarianism
vegetarians
vegetation
vehement
vehemently
vehicle
vehicles
veil
veiled
veiling
veils
vein
veined
veining
veins
velocities
velocity
velour
velvet
velvetier
velvetiest
velvety
vend
vended
vender
venders
vending
vendor
vendors
vends
veneer
veneered
veneering
veneers
venerable
venerate
venerated
venerates
venerating
veneration
vengeance
vengeful
venison
venom
venomous
vent
vented
ventilate
ventilated
ventilates
ventilating
ventilation
ventilator
ventilators
venting
ventricle
ventricles
ventriloquist
ventriloquists
vents
venture
ventured
ventures
venturing
venue
venues
veracity
veranda
verandah
verandahs
verandas
verb
verbal
verbally
verbals
verbatim
verbiage
verbose
verbosity
verbs
verdict
verdicts
verge
verged
verges
verging
verier
veriest
verification
verified
verifies
verify
verifying
veritable
vermin
vernacular
vernaculars
versatile
versatility
verse
versed
verses
versing
version
versions
versus
vertebra
vertebrae
vertebras
vertebrate
vertebrates
vertical
vertically
verticals
vertices
vertigo
verve
very
vessel
vessels
vest
vested
vestibule
vestibules
vestige
vestiges
vesting
vestment
vestments
vests
vet
veteran
veterans
veterinarian
veterinarians
veterinaries
veterinary
veto
vetoed
vetoes
vetoing
vets
vetted
vetting
vex
vexation
vexations
vexed
vexes
vexing
via
viability
viable
viaduct
viaducts
vial
vials
vibrant
vibrate
vibrated
vibrates
vibrating
vibration
vibrations
vicar
vicarious
vicariously
vicars
vice
viced
vices
vicing
vicinity
vicious
viciously
victim
victimize
victimized
victimizes
victimizing
victims
victor
victories
victorious
victors
victory
video
videos
videotape
videotaped
videotapes
videotaping
vie
vied
vies
view
viewed
viewer
viewers
viewing
viewpoint
viewpoints
views
vigil
vigilance
vigilant
vigilante
vigilantes
vigils
vigor
vigorous
vigorously
vile
viler
vilest
vilified
vilifies
vilify
vilifying
villa
village
villager
villagers
villages
villain
villainies
villainous
villains
villainy
villas
vindicate
vindicated
vindicates
vindicating
vindictive
vine
vinegar
vines
vineyard
vineyards
vintage
vintages
vinyl
vinyls
viola
violas
violate
violated
violates
violating
violation
violations
violence
violent
violently
violet
violets
violin
violins
viper
vipers
viral
virgin
virginity
virgins
virile
virility
virtual
virtually
virtue
virtues
virtuosi
virtuoso
virtuosos
virtuous
virtuously
virulent
virus
viruses
visa
visaed
visaing
visas
vise
vised
vises
visibility
visible
visibly
vising
vision
visionaries
visionary
visioned
visioning
visions
visit
visitation
visitations
visited
visiting
visitor
visitors
visits
visor
visors
vista
vistas
visual
visualize
visualized
visualizes
visualizing
visually
visuals
vital
vitality
vitally
vitamin
vitamins
vitriolic
vivacious
vivaciously
vivacity
vivid
vivider
vividest
vividly
vivisection
vizor
vizors
vocabularies
vocabulary
vocal
vocalist
vocalists
vocals
vocation
vocational
vocations
vociferous
vociferously
vodka
vogue
vogues
voice
voiced
voices
voicing
void
voided
voiding
voids
volatile
volcanic
volcano
volcanoes
volcanos
volition
volley
volleyball
volleyballs
volleyed
volleying
volleys
volt
voltage
voltages
volts
volume
volumes
voluminous
voluntaries
voluntarily
voluntary
volunteer
volunteered
volunteering
volunteers
voluptuous
vomit
vomited
vomiting
vomits
voodoo
voodooed
voodooing
voodoos
voracious
vortex
vortexes
vortices
vote
voted
voter
voters
votes
voting
vouch
vouched
voucher
vouchers
vouches
vouching
vow
vowed
vowel
vowels
vowing
vows
voyage
voyaged
voyager
voyagers
voyages
voyaging
vulgar
vulgarer
vulgarest
vulgarities
vulgarity
vulnerabilities
vulnerability
vulnerable
vulture
vultures
vying
wad
wadded
wadding
waddle
waddled
waddles
waddling
wade
waded
wades
wading
wads
wafer
wafers
waffle
waffled
waffles
waffling
waft
wafted
wafting
wafts
wag
wage
waged
wager
wagered
wagering
wagers
wages
wagged
wagging
waging
wagon
wagons
wags
waif
waifs
wail
wailed
wailing
wails
waist
waistline
waistlines
waists
wait
waited
waiter
waiters
waiting
waitress
waitresses
waits
waive
waived
waiver
waivers
waives
waiving
wake
waked
waken
wakened
wakening
wakens
wakes
waking
walk
walked
walker
walkers
walking
walkout
walkouts
walks
wall
walled
wallet
wallets
walling
wallop
walloped
walloping
wallops
wallow
wallowed
wallowing
wallows
wallpaper
wallpapered
wallpapering
wallpapers
walls
walnut
walnuts
walrus
walruses
waltz
waltzed
waltzes
waltzing
wan
wand
wander
wandered
wanderer
wanderers
wandering
wanders
wands
wane
waned
wanes
waning
wanna
wanner
wannest
want
wanted
wanting
wanton
wantoned
wantoning
wantons
wants
war
warble
warbled
warbles
warbling
ward
warded
warden
wardens
warding
wardrobe
wardrobes
wards
warehouse
warehoused
warehouses
warehousing
warfare
warhead
warheads
warier
wariest
warlike
warm
warmed
warmer
warmest
warming
warmly
warms
warmth
warn
warned
warning
warnings
warns
warp
warpath
warpaths
warped
warping
warps
warrant
warranted
warrantied
warranties
warranting
warrants
warranty
warrantying
warred
warren
warrens
warring
warrior
warriors
wars
wart
wartime
warts
wary
was
wash
washable
washables
washcloth
washcloths
washed
washer
washers
washes
washing
washout
washouts
washroom
washrooms
wasp
wasps
wastage
waste
wastebasket
wastebaskets
wasted
wasteful
wastefully
wasteland
wastelands
wastes
wasting
watch
watchdog
watchdogs
watched
watches
watchful
watching
watchman
watchmen
watchword
watchwords
water
watercolor
watercolors
watered
waterfall
waterfalls
waterfront
waterfronts
waterier
wateriest
watering
waterlogged
watermark
watermarked
watermarking
watermarks
watermelon
watermelons
waterproof
waterproofed
waterproofing
waterproofs
waters
watershed
watersheds
watertight
waterway
waterways
waterworks
watery
watt
watts
wave
waved
waveform
wavelength
wavelengths
waver
wavered
wavering
wavers
waves
wavier
waviest
waving
wavy
wax
waxed
waxes
waxier
waxiest
waxing
waxy
way
waylaid
waylay
waylaying
waylays
ways
wayside
waysides
wayward
we
weak
weaken
weakened
weakening
weakens
weaker
weakest
weakling
weaklings
weakly
weakness
weaknesses
wealth
wealthier
wealthiest
wealthy
wean
weaned
weaning
weans
weapon
weaponry
weapons
wear
wearied
wearier
wearies
weariest
wearily
weariness
wearing
wearisome
wears
weary
wearying
weasel
weaseled
weaseling
weasels
weather
weathered
weathering
weathers
weave
weaved
weaver
weavers
weaves
weaving
web
webbed
webbing
webs
wed
wedded
wedder
wedding
weddings
wedge
wedged
wedges
wedging
wedlock
weds
wee
weed
weeded
weedier
weediest
weeding
weeds
weedy
weeing
week
weekday
weekdays
weekend
weekended
weekending
weekends
weeklies
weekly
weeks
weep
weeping
weeps
weer
wees
weest
weigh
weighed
weighing
weighs
weight
weighted
weightier
weightiest
weighting
weights
weighty
weird
weirder
weirdest
weirdness
weirdo
weirdos
welcome
welcomed
welcomes
welcoming
weld
welded
welder
welders
welding
welds
welfare
well
welled
welling
wellington
wells
welt
welted
welter
weltered
weltering
welters
welting
welts
went
wept
were
werewolf
werewolves
west
westerlies
westerly
western
westerns
westward
wet
wets
wetted
wetter
wettest
wetting
whack
whacked
whacking
whacks
whale
whaled
whaler
whalers
whales
whaling
wharf
wharfs
wharves
what
whatever
whats
whatsoever
wheat
wheedle
wheedled
wheedles
wheedling
wheel
wheelbarrow
wheelbarrows
wheelchair
wheelchairs
wheeled
wheeling
wheels
wheeze
wheezed
wheezes
wheezing
when
whence
whenever
whens
where
whereabouts
whereas
whereby
wherein
wheres
whereupon
wherever
wherewithal
whet
whether
whets
whetted
whetting
whew
which
whichever
whiff
whiffed
whiffing
whiffs
while
whiled
whiles
whiling
whilst
whim
whimper
whimpered
whimpering
whimpers
whims
whimsical
whine
whined
whines
whining
whinnied
whinnies
whinny
whinnying
whip
whipped
whipping
whips
whir
whirl
whirled
whirling
whirlpool
whirlpools
whirls
whirlwind
whirlwinds
whirr
whirred
whirring
whirrs
whirs
whisk
whisked
whisker
whiskered
whiskers
whiskey
whiskeys
whiskies
whisking
whisks
whisky
whiskys
whisper
whispered
whispering
whispers
whistle
whistled
whistles
whistling
white
whiten
whitened
whitening
whitens
whiter
whites
whitest
whitewash
whitewashed
whitewashes
whitewashing
whittle
whittled
whittles
whittling
whiz
whizz
whizzed
whizzes
whizzing
who
whoa
whoever
whole
wholehearted
wholeheartedly
wholes
wholesale
wholesaled
wholesaler
wholesalers
wholesales
wholesaling
wholesome
wholly
whom
whoop
whooped
whooping
whoops
whopper
whoppers
whore
whores
whose
why
whys
wick
wicked
wickeder
wickedest
wickedly
wickedness
wicker
wickers
wicket
wickets
wicks
wide
widely
widen
widened
widening
widens
wider
widespread
widest
widow
widowed
widower
widowers
widowing
widows
width
widths
wield
wielded
wielding
wields
wife
wig
wigged
wigging
wiggle
wiggled
wiggles
wiggling
wigs
wigwam
wigwams
wild
wildcat
wildcats
wildcatted
wildcatting
wilder
wilderness
wildernesses
wildest
wildfire
wildfires
wildlife
wildly
wildness
wilds
wilful
wilfully
wilier
wiliest
will
willed
willful
willfully
willing
willingly
willingness
willow
willows
willpower
wills
wilt
wilted
wilting
wilts
wily
win
wince
winced
winces
winch
winched
winches
winching
wincing
wind
winded
windfall
windfalls
windier
windiest
winding
windmill
windmilled
windmilling
windmills
window
windowing
windowpane
windowpanes
windows
windpipe
windpipes
winds
windscreen
windscreens
windshield
windshields
windy
wine
wined
wines
wing
winged
wingers
winging
wings
wining
wink
winked
winking
winks
winner
winners
winning
winnings
wins
winsome
winsomer
winsomest
winter
wintered
winterier
winteriest
wintering
winters
wintertime
wintery
wintrier
wintriest
wintry
wipe
wiped
wiper
wipers
wipes
wiping
wire
wired
wires
wirier
wiriest
wiring
wiry
wisdom
wise
wisecrack
wisecracked
wisecracking
wisecracks
wisely
wiser
wises
wisest
wish
wishbone
wishbones
wished
wishes
wishful
wishing
wisp
wispier
wispiest
wisps
wispy
wist
wistful
wistfully
wit
witch
witchcraft
witched
witches
witching
with
withdraw
withdrawal
withdrawals
withdrawing
withdrawn
withdraws
withdrew
wither
withered
withering
withers
withheld
withhold
withholding
withholds
within
without
withstand
withstanding
withstands
withstood
witless
witness
witnessed
witnesses
witnessing
wits
witticism
witticisms
wittier
wittiest
witting
witty
wive
wives
wiz
wizard
wizards
wizened
wizes
wizzes
wobble
wobbled
wobbles
wobblier
wobbliest
wobbling
wobbly
woe
woes
wok
woke
woken
woks
wolf
wolfed
wolfing
wolfs
wolves
woman
womanhood
womankind
womb
wombat
wombats
wombs
women
won
wonder
wondered
wonderful
wonderfully
wondering
wonderland
wonderlands
wonders
wondrous
wont
woo
wood
woodchuck
woodchucks
wooded
wooden
woodener
woodenest
woodier
woodies
woodiest
wooding
woodland
woodlands
woodpecker
woodpeckers
woods
woodsman
woodsmen
woodwind
woodwinds
woodwork
woody
wooed
woof
woofed
woofing
woofs
wooing
wool
woolen
woolens
woolie
woolier
woolies
wooliest
woollier
woollies
woolliest
woolly
wooly
woos
word
worded
wordier
wordiest
wording
wordings
words
wordy
wore
work
workable
workbench
workbenches
workbook
workbooks
worked
worker
workers
workforce
working
workings
workload
workman
workmanship
workmen
workout
workouts
workplace
works
workshop
workshops
workstation
workstations
world
worldlier
worldliest
worldly
worlds
worldwide
worm
wormed
wormhole
wormholes
worming
worms
worn
worried
worries
worrisome
worry
worrying
worse
worsen
worsened
worsening
worsens
worship
worshiped
worshiper
worshipers
worshiping
worshipped
worshipper
worshippers
worshipping
worships
worst
worsted
worsting
worsts
worth
worthier
worthies
worthiest
worthless
worthwhile
worthy
wot
would
woulds
wound
wounded
wounder
wounding
wounds
wove
woven
wow
wowed
wowing
wows
wrangle
wrangled
wrangler
wranglers
wrangles
wrangling
wrap
wrapped
wrapper
wrappers
wrapping
wrappings
wraps
wrapt
wrath
wreak
wreaked
wreaking
wreaks
wreath
wreathe
wreathed
wreathes
wreathing
wreaths
wreck
wreckage
wrecked
wrecker
wrecking
wrecks
wren
wrench
wrenched
wrenches
wrenching
wrens
wrest
wrested
wresting
wrestle
wrestled
wrestler
wrestlers
wrestles
wrestling
wrests
wretch
wretched
wretcheder
wretchedest
wretches
wrier
wriest
wriggle
wriggled
wriggles
wriggling
wright
wring
wringer
wringers
wringing
wrings
wrinkle
wrinkled
wrinkles
wrinkling
wrist
wrists
wristwatch
wristwatches
writ
writable
write
writer
writers
writes
writhe
writhed
writhes
writhing
writing
writings
writs
written
wrong
wrongdoer
wrongdoers
wrongdoing
wrongdoings
wronged
wronger
wrongest
wronging
wrongly
wrongs
wrote
wrought
wrung
wry
wryer
wryest
xenophobia
xylophone
xylophones
yacht
yachted
yachting
yachts
yack
yacked
yacking
yacks
yak
yakked
yakking
yaks
yam
yams
yank
yanked
yanking
yanks
yap
yapped
yapping
yaps
yard
yards
yardstick
yardsticks
yarn
yarns
yawn
yawned
yawning
yawns
year
yearlies
yearling
yearlings
yearly
yearn
yearned
yearning
yearnings
yearns
years
yeast
yeasts
yell
yelled
yelling
yellow
yellowed
yellower
yellowest
yellowing
yellows
yells
yelp
yelped
yelping
yelps
yen
yens
yes
yeses
yessed
yessing
yesterday
yesterdays
yet
yeti
yew
yews
yield
yielded
yielding
yields
yock
yocks
yodel
yodeled
yodeling
yodelled
yodelling
yodels
yoga
yoghourt
yoghourts
yoghurt
yoghurts
yogurt
yogurts
yoke
yoked
yokel
yokels
yokes
yoking
yolk
yolks
yonder
you
young
younger
youngest
youngster
youngsters
your
yours
yourself
yourselves
yous
youth
youthful
youths
yowl
yowled
yowling
yowls
yuck
yucks
zanier
zanies
zaniest
zany
zeal
zealous
zebra
zebras
zenith
zeniths
zero
zeroed
zeroes
zeroing
zeros
zest
zests
zeta
zigzag
zigzagged
zigzagging
zigzags
zillion
zillions
zinc
zinced
zincing
zincked
zincking
zincs
zip
zipped
zipper
zippered
zippering
zippers
zipping
zips
zodiac
zodiacs
zombi
zombie
zombies
zombis
zone
zoned
zones
zoning
zoo
zoological
zoologist
zoologists
zoology
zoom
zoomed
zooming
zooms
zoos
zucchini
zucchinis
""".split('\n')

SPAMS = """
Gbqnl'f fcnz:

V jnf fhecevfrq, gbb!
Jub_pbhyq_fhfcrpg_fbzrguvat_yvxr_gung? fuvglvvvvv
%
Gbqnl'f fcnz:

qbag or n ybaryl snggl ng ubzr
%
Gbqnl'f fcnz:

tb uneq gur purnc jnl
%
Gbqnl'f fcnz:

GFHANZV IVPGVZF NVQF NCCRNY
%
Gbqnl'f fcnz:

N yngrfg ivrj fubjf gung 75 % bs tveyf ner hafngvfsvrq
jvgu gurve frkhny cnegaref. Bs pbhefr ovt cneg bs gurfr jbzra
jbhyq arire pbairl gurve orggre unysf gung gurl ner vyy-sngrq.
%
Gbqnl'f fcnz:

Anzr: FrklPevfgl
Ntr: 25
Ybpngvba: Arj Lbex
Zrffntr: V'z gverq bs orvat zneevrq naq abj V jnag fbzr sha :)
         V'z ybbxvat sbe n qvfperrg zna, fvatyr be zneevrq.
         Jr pna pung n juvyr, vs lbh jnag. V'z bcra gb rirelguvau...
         V jnag gb purng ba zl uhfonaq :))
         Fraq zr lbhe cvpgher, yrg'f qngr.
%
Gbqnl'f fcnz:

Frkhny fngvfsnpgvba vf bayl ba pyvpx njnl
%
Gbqnl'f fcnz:

FRKHNYYL-RKCYVPVG: Fur cynprf naq beqre naq jnvgf sbe ure SERR FNHFNTR!
%
Gbqnl'f fcnz:

Ubj qb lbh qb, yrg zr cerfrag sbe lbh bhe Arjrfg tnyrevnf.

Bar bs gur zbfg ornhgvshy cntr ba gur cynarg vf jura n
ubg pragresbyq tvey gheaf ure onpx gb lbh naq oraqf bire
naq fybjyl chyyf bss ure _cnagf_!
%
Gbqnl'f fcnz:

Gurfr gnoyrgf ner n va n fpvragvsvp jnl sbeznyvfrq ureonprbhf
ahgevgvbany oyraq gb raunapr nohaqnapr ol orggrevat fcrez pryy
pynff, ahzore naq zbgvba.
%
Gbqnl'f fcnz:

Qbjaybnq nqh1g qiq zbivrf gb lbhe ubzr pbzchgre!
Lbh trg bar jrrx S E R R jvgu 100% pbzcyrgr npprff!
GUVF VF GUR QIQ FVGR BS LBHE QNEXRFG QERNZF!
Ohea gurz gb PQf pbyyrpg gurz be genqr gurz jr qba'g pner!
Orybj ner fbzr fnzcyr fperraf sebz qiq zbivrf jr unir!

    Yrfovna Guerrfbzr
    Nfvna Pbpx Fhpxvat
    Shpx Zl Gvtug Nff

Jr tbg zber gura 2000 qvssrerag nqh1g qiqf sbe vafgnag qbjaybnq!
Ivfvg hf urer gb fgneg lbhe S E R R qiq qbjaybnq gbqnl!
%
Gbqnl'f fcnz:

Rerpgv1r Qlfshapgvba (RQ) vf n pbaqvgvba gung nssrpgf fbzr zra. Vg vf
gur vanovyvgl gb trg be znvagnva na rerpg1ba sbe fngvfsnpgbel f3k.
Pbzzbayl xabja nf vzc0grapr
Gerng guvf sbe $ 1.74 N qbfr!!
Lbh naq lbhe jvsr obgu qrfreir vg.
%
Gbqnl'f fcnz:

qhxrqbz Lhbaat naq ornhggvshVV Grrraf syhggre
%
Gbqnl'f fcnz:

Unvsn, Srnghevat 80,000+ Nzznmvat RkppVhffvir Cyfpgher & Ivqf
bs Gur Lhbat Grrra ZbqrVf nethzrag

JrVpbzr gb gur ErnV Rqra

Fvtaben, Ubeeaal natry ornnhggvrf ner ratebffrq va nyy cbffvoyr
qryvtugf naq ibyhcghbhfarff rireljurer
%
Gbqnl'f fcnz:

Pbjf Unir Iryirgl Gbathrf
%
Gbqnl'f fcnz:

fubbg zber ph`z guna fur pna qevax
%
Gbqnl'f fcnz:

Vapernfr lbhe PHZ I0YHZR, naq 0etnfz Yratgu
znva oravsvgf:
- Gur ybatrfg zbfg vagrafr Betnfzf bs lbhe yvsr
- Repgvbaf yvxr fgrry
- yapernfrq yvovqb/qrfver
- Fgebatre rwnphyngba (jngpu jurer lbhe nvzvat)
- Zhygvcyr 0etnfzf
- Hc gb 5BB% zber ibyhzr (pbire ure va vg vs lbh jnag)
- Fghqvrf fubj vg gnfgrf fjrrgre
QVFPERRG FNZR QNL FUVCCVAT - GEL VG, L0H'YY Y0IR VG!
(naq fur'yy gunax lbh sbe vg)
%
Gbqnl'f fcnz:

c#vyy gb vzceb'ir ph#z synibhe naq i`byhzr
%
Gbqnl'f fcnz:

Trg n qngr jvgu n anhtugl tvey be thl
%
Gbqnl'f fcnz:

Fvpx naq gverq bs orvat fvatyr?
Ner lbh naablrq ol lbhe tveysevraq be jvsr
Svaq n arj qngr gbqnl.
Zvyyvbaf bs cebsvyrf bs crbcyr ybpny gb lbhe nern ybbxvat sbe sha.
Svaq n qngr sbe gur avtug be frnepu sbe lbhe arkg jvsr.

Znal ner irel anhtugl naq jnag gb ubbx hc sbe fbzr pnfhny obbz obbz.
Zrrg fbzrbar arj, evtug abj.

Naq vg qbrfag pbfg n guvat gb wbva va gur sha.
%
Gbqnl'f fcnz:

PELVAT SBE URYC
%
Gbqnl'f fcnz:

fc3:ez (ph;z) i_0yhz'r cyYY;f
- rwnphhyngr yvxr arire orsber.
- betfzf yvxr lbh'ir arire unq.
- oybj yvxr n ubefr nyy bire ure.

%
Gbqnl'f fcnz:

Trg rerpg gbqnl!
%
Gbqnl'f fcnz:

Url Mnpunel ,

Pbzvat sebz n jbznaf ivrj vg vf vzcbegnag gung n zna pna ynfg.
Ubj jbhyq lbh srry vs lbhe jbzna pbhyq bayl shpx sbe 2 zvahgrf?

Arire yrg ure qbja ntnva. Cvpx hc fbzr ivnten be pvnyvf naq
ynfg ybatre gura fur qbrf!

Jung qb lbh unir gb ybfr?? Pyvpx gur yvax sbe zber vasb.

Lbhef,
Crghyn
%
Gbqnl'f fcnz:

LBHE RZNVY JBA N CEVMR.
%
Gbqnl'f fcnz:

 _     _   _   _____   _____   _____   _   __   _
| |   / / | | /  ___| /  _  \ |  _  \ | | |  \ | |
| |  / /  | | | |     | | | | | | | | | | |   \| |
| | / /   | | | |     | | | | | | | | | | | |\   |
| |/ /    | | | |___  | |_| | | |_| | | | | | \  |
|___/     |_| \_____| \_____/ |_____/ |_| |_|  \_|

whfg bar pyvpx njnl

Va frnepu bs Jvg gurfr ybfr gurve pbzzba Frafr,
%
Gbqnl'f fcnz:

shpx yvxr navznyf
%
Gbqnl'f fcnz:

Abguvat'f pregnva va guvf jbeyq. Jryy, rkprcg sbe bar guvat.
Jura lbh'er ernql gb fubbg LBHE ybnq, gurer'f n ubggvr ubr
jvgu ure zbhgu bcra.
Fur'yy pngpu nyy lbh tbg. Naq ort sbe zber.

Pyvpx urer sbe fbzr terng phzfubg npgvba
%
Gbqnl'f fcnz:

Lbh'er n Gnfgl Gerng
%
Gbqnl'f fcnz:

Uv Qnqql

pbzr jngpu zr  naq zl tveyf .... yvpxvta gur t-fcbg
furf   pernzzzrq nyy bire zl  snpr

Yvpx  zr abj

Ybir lbh,
Wraal
%
Gbqnl'f fcnz:

guvf vf gur bayvar cynpr sbe chffl
%
Gbqnl'f fcnz:

1fg bss lbh trg n ggg0yyl cue rrr gevny sbe guvf qnza guvat.
Frpbaq, guvf cynpr vf rkpryyrag sbe jura lbh rvgure jnag gb zrrg
rvgure tveyyf gung ner gbgnyyl f1hggllll, jnag gb whfg trg vg ba,
jnag thlf gung ner bgure guna gur thlf gung gurl ner hfrq gbb,
be sbe gbgnyyl ubea rr ubhffrjviirf gung jnag gb trg vg tbvat
jvgu bgure thlf juvyr gurve uhoolvrf ner bhg.
Vg'f sbe bar vg'f sbe nyy vg'f sbenalbar gung ernyyl jnagf gb trg
fbzrguvat tbvat sbe whfg gung fbeg bs guvat. Bx abj purpx guvf bhg...
%
Gbqnl'f fcnz:

Guvf vf n cerggl tbbq guvatjr'er nqqlvat gb lbh urer orpnhfr lbh trg
qvnzbaqf ba gur fbhyf bs lbhe fubrf. vs lbh guvax gung lbh jbhyq yvxr
gb fgbc trggvat guvf penc sebz hf gura nyy lbh arrq gb qb gb trg bhg
sebz bhe nb|iregvfzragf vf urer
%
Gbqnl'f fcnz:

Yvfgra, lbh'er tbvat gb yvxr vg.  Qb guvf.  Fb qba'g qbhog zr.
Be lbh jvyy trg irel greevoyr jnegf.  Naq unir vagrfgvany cnenfvgrf
gung pnhfr rkcybfvir qvnuerrrun.  Naq gung jvyy or irel onq naq
lbh jvyy pel naq abgvxr gur vagrearg orpnhfr bs vg.
Gunax lbh naq unir n irel avpr qnl jvgu lbhefrys.
Gunaxf, Gurqhqrf
%
Gbqnl'f fcnz:

Ybaryl nzngrhef va lbhe nern
Zhygvcyr tveyf  ernql gb zrrg lbh .
Obhapvat onorf ybbxvat sbe  zrng.
Naq, ubggvrf jvyyvat gb unir nany frk.

Jvgu lbh.

Jbegu n ohpx? Shpx lrnu!
%
Gbqnl'f fcnz:

Frnepuvat sbe orfg nqhyg qng1at f1gr?
Pyvpx u3er a0j naq wb1a sbe ser3!
%
Gbqnl'f fcnz:

Er: V qrfgeblrq guvf VvggVr fVhhgf snpr vaqjryy      ragnvy
%
Gbqnl'f fcnz:

  Lhbat   Nzzrevpna   Onnorf Ahhqr,      thvgne'f
     Fppubbby TveeVf   naq PuurreVrnqref, noreengvbaf

Ceyingr     PbVVrpgvba ${FvgrHEY}

 Ireel FcrppvnV     Lbhhaat  UneV)pber,  nevqvgl
%
Gbqnl'f fcnz:

lbh ybbx yvxr na ncr!
%
Gbqnl'f fcnz:

Lbhe cubgb, hnuuu.... , lbh ner anxrq!
%
Gbqnl'f fcnz:

UNPX BAYL SBE $ 20 Pbagnpg ng rznvy ${HfreAnzr}@ubgznvy.pbz nqq zr
gbqnl gb lbhe zfa pbagnpgf naq fgneg unpxvat nalbar.
%
Gbqnl'f fcnz:

P4zreba Q1nm c0ea 4serr
%
Gbqnl'f fcnz:

Unir lbh frra rirel Cnevf Uvygba frk gncr znqr lrg?
Lbh unir gb purpx vg bhg vgf n serr naq zhpu zber!
Purpx ure bhg urer
%
Gbqnl'f fcnz:

Orpbzr N yrguny Jrncba genvarq ol Ehffvna XTO ntragf!
%
Gbqnl'f fcnz:

Yrnea Gur Gehr Frpergf Bs Frys Qrsrafr Naq Unir Na Hasnve Nqinagntr
Bire Nal Nggnpxre Jvgu Nal Jrncbaf!
Sbe gur svefg gvzr va gur uvfgbel gur Ehffvna Fcrpvny Sbeprf bcra
gurve frpergf gb gur pvivyvnaf!
%
Gbqnl'f fcnz:

Tbbqqnl. Gurfr Arrqshy ynqvrf jbhyq yvxr fbzrbar gb onat gurz
%
Gbqnl'f fcnz:

LB lb. Jung jbhyq yvxr va lbhe yvsr? N tbbq gvzr gbavtug.
Fjrrg ybir.  Frk.  Pbzcnavbafuvc.  Arneyl nyy bs gurfr Ybaryl zbguref
jnag fbzrbar gb gnxr pner bs gurz. Pna'g jnvg gb gnyx gb lbh ntnva.
%
Gbqnl'f fcnz:

fpubbyoblvfu nat ubeal lbhat ynqvrf ner ubyqvat bss lbh!

V unir tbg zber gura 10.000 fvatyr grrantr rkcyvpvg
rkcbfherf naq nobhg 70 ubhef bs rknygrq fryrpg ivqrbf.
%
Gbqnl'f fcnz:

Er : Cerggl obl jnagf gb zrrg n zngher jbzna
%
Gbqnl'f fcnz:

SNPG: Va n cbyy pbaqhpgrq ol n pbatybzrengr bs znwbe pbaqbz
znahsnpgheref bire 80% bs jbzra ner hafngvfsvrq jvgu gurve cnegaref
fvmr naq frkhny cresbeznapr.

FBYHGVBA: Ol gnxvat Angheny Encvq Tebjgu Sbezhyn lbh jvyy or noyr
gb pbageby ubj ovt lbh trg.
N uhtr urnygul znaubbq vf gur onfvf bs nggenpgvba naq ncgvghqr
sbe jbzra.
Gurer vf ab ernfba gung lbh fubhyqa'g unir n srj vapurf ba
gur pbzcrgvgvba!!
Jnag gb zber QRGNVYF????
%
Gbqnl'f fcnz:

Frkhnyyl bhgcresbez nalbar va gur jbeyq!
%
Gbqnl'f fcnz:

Gur C0eabRkge4intnamn

Jngpu nyy gur Anhtugl Cnevf Uvygba Sbbgntr rire pnhtug ba gncr!
Naq Inevbhf Njneq jvaavat Fgernzvat QIQF naq zhpu zber!

Fvta Hc sbe n Serr Gevny Abj!
%
Gbqnl'f fcnz:

Lbh ner orvat svyzrq!
%
Gbqnl'f fcnz:

Gur jbeyq'f svefg Vagrearg puhepu unf snyyra ivpgvz gb n cynthr bs
iveghny qrzbaf, fbzr bs jubz unir orra ybttvat ba nf Fngna naq
hayrnfuvat fgevatf bs rkcyrgvirf qhevat frezbaf.
Gur gbc Nzrevpna trareny va Nstunavfgna unf beqrerq n fjrrcvat
erivrj bs frpergvir H.F. wnvyf va gur pbhagel nzvq zbhagvat
nyyrtngvbaf bs cevfbare nohfr, n zvyvgnel fcbxrfzna fnvq Jrqarfqnl.

Gur puvcznxre cnqf vgf bssrevatf sbe 2C naq 4C cyngsbezf jvgu na
rlr gb gur shgher.

Fjbbfvr Xhegm bs Sebmra naq Enhy Rfcnemn bs Gur Abezny Urneg jvyy
ubfg gur 2004 Bovr Njneqf prerzbal ba Znl 17 ng Jrofgre Unyy.
%
Gbqnl'f fcnz:

fubbg ohpxrg ybnqf bs fcrez
%
Gbqnl'f fcnz:

fubbg zber fcr"ez guna fur pna qevax
%
Gbqnl'f fcnz:

Guvatf crbcyr arrq sbe rerpgvba qlfshap..
%
Gbqnl'f fcnz:

Jnvgvat sbe na ubhe be zber gb trg ernql gb znxr ybir gb lbhe cnegare
vf irel shfgengvat, rfcrpvnyyl gvzr vf ntnvafg lbh.

Jryy, 15 zvahgrf vf ernyyl nyy lbh arrq. Snfg? jryy fbzrgvzrf sbercynl
gnxrf ybatre guna gung.

Jul qbag lbh cebir gurz lbhefrys.
%
Gbqnl'f fcnz:

Qb abg ivfvg guvf vyyrtny jrofvgrf!
%
Gbqnl'f fcnz:

Svefg gvzr nany - tveyf ybir vg
%
Gbqnl'f fcnz:

jvpxrq qevtf sbe lbh
%
Gbqnl'f fcnz:

lryybj cvffff
%
Gbqnl'f fcnz:

Pernzl thfuref
%
Gbqnl'f fcnz:

V zrg zr {qvf|guvf} {puvpxvr|tveyvr}, fur gubhtug V jnf evpu.
V {uvg|gnccrq} vg nyy avtug ybat.

{Abar bs hf jvyy rirel nppbzcyvfu nalguvat rkpryyrag be pbzznaqvat
rkprcg jura ur yvfgraf gb guvf juvfcre juvpu vf urneq ol uvz nybar. |Vg
qbrf abg qb gb qjryy ba qernzf naq sbetrg gb yvir.  }
%
Gbqnl'f fcnz:

Wrerzl

irel uvtr   turggb   qvpxf,  gurerf   ynetr naq oybjvat  bhg   juvgr
ubrf  chfflf
%
Gbqnl'f fcnz:

Zbz yvrq gb zr !

Zbgure jnf jebat! Zbarl qbrf tebj ba gerrf!

Lrc .zl zbgure yvrq gb zr.
Fur gbyq zr gung V unq gb jbex 40 ubhef n qnl sbe 40 lrnef gb ergver
unccl naq fhpprffshy.

Uzzzzzz fur qvqa'g ergver unccl naq fhpprffshy.

Naq gura, nf vs ure svefg yvr jnfa'g onq rabhtu,
V sbhaq bhg gung zbarl qbrf tebj ba gerrf,

Naq nyy V unir gb qb vf fubj hc,
Naq qb n yvggyr jbex cvpxvat n onfxrgshy.
Urer vf jurer gur gerr vf:
%
Gbqnl'f fcnz:

"Zl tveysevraq ybirf gur erfhygf, ohg fur qbrfa'g xabj jung V qb.
Fur guvaxf vg'f angheny" -Gubznf, PN

"V'ir orra hfvat lbhe cebqhpg sbe 4 zbaguf abj. V'ir vapernfrq
zl yratgu sebz 2" gb arneyl 6" .
Lbhe cebqhpg unf fnirq zl frk yvsr." -Zngg, SY

Cyrnfher lbhe cnegare rirel gvzr jvgu n ovttre, ybatre, fgebatre Havg
Ernyvfgvp tnvaf dhvpxyl

gb or n fghq cerff urer
%
Gbqnl'f fcnz:

Uv

Arj zrqvpngba yrgf lbh chzc ure 5-1B gvzrf ybatre

YyZyGRQ GEyNY: $6B/ogy (0eqre qvfcngpurq fnzr qnl)
%
Gbqnl'f fcnz:

p`hz jura h jnag'
%
Gbqnl'f fcnz:

PBATENGHYNGVBAF LBH UNIR JBA JBA $500,000:00!!!
%
Gbqnl'f fcnz:

PBATENGHYNGVBAF LBH UNIR JBA JBA $500,000:00!!!
YHPXL QNL VAGREANGVBANY NJNEQ AY.
NQQ:QNNJREX 100N,1103XN
NZFGREQNZ.(GUR ARGUREYNAQF)
SEBZ GUR QRFX BS GUR QVERPGBE VAGREANGVBANY CEBZBGVBA/CEVMR NJNEQ QRCG.
%
Gbqnl'f fcnz:

Lbh tbg Fcljner
%
Gbqnl'f fcnz:

Gurer'f n 95 punapr lbhe CP vf vasrpgrq jvgu Fcljner!

Fcljner , zhpu yvxr n ivehf, vf n znyvpvbhf fbsgjner cynagrq ba lbhe
pbzchgre.

Vg pna:
* Fgrny lbhe cnffjbeqf
* Fgrny lbhe vqragvgl
* Fcnz lbhe rznvy nppbhag
* Penfu lbhe pbzchgre
* Obzoneq lbh jvgu nqiregvfvat
* Fgrny lbhe perqvg pneq ahzoref
* Qbjaybnq lbhe Cevingr svyrf
* Zbavgbe lbhe rznvyf & XrlFgebxrf
* Jngpu gur fvgrf lbh ivfvg
naq zber...

CEBGRPG LBHEFRYS!
%
Gbqnl'f fcnz:

100x+ jbzra gung jnag gb unir frk
%
Gbqnl'f fcnz:

Qrne ,

V nz Zef. Fhun Nensng, gur jvsr bs Lnffre Nensng, gur Cnyrfgvavna
yrnqre jub qvrq erpragyl va Cnevf.  Fvapr uvf qrngu naq rira cevbe
gb gur naabhaprzrag, V unir orra guebja vagb n fgngr bs nagntbavfz,
pbashfvba, uhzvyvngvba, sehfgengvba naq ubcryrffarff ol gur cerfrag
yrnqrefuvc bs gur Cnyrfgvavna Yvorengvba Betnavmngvba naq gur arj
Cevzr Zvavfgre.  V unir rira orra fhowrpgrq gb culfvpny naq
cflpubybtvpny gbegher.  Nf n jvqbj gung vf fb genhzngvmrq, V unir ybfg
pbasvqrapr jvgu rirelobql va gur pbhagel ng gur zbzrag.

Lbh zhfg unir urneq bire gur zrqvn ercbegf naq gur Vagrearg ba gur
qvfpbirel bs fbzr shaq va zl uhfonaq frperg onax nppbhag naq pbzcnavrf
naq gur nyyrtngvbaf bs fbzr uhtr fhzf bs zbarl qrcbfvgrq ol zl uhfonaq
va zl anzr bs juvpu V unir ershfrf gb qvfpybfr be tvir hc gb gur
pbeehcg Cnyrfgvar Tbireazrag.

Va snpg gur gbgny fhz nyyrtrqyl qvfpbirerq ol gur Tbireazrag fb sne
vf va gur ghar bs nobhg $6.5 Ovyyvba Qbyynef.  Naq gurl ner abg
eryragvat ba gurve rssbeg gb znxr zr cbbe sbe yvsr.  Nf lbh xabj, gur
Zbfyrz pbzzhavgl unf ab ertneqf sbe jbzna, zber vzcbegnagyl jura gur
jbzna vf sebz n Puevfgvna onpxtebhaq, urapr zl qrfver sbe n sbervta
nffvfgnapr.

V unir qrcbfvgrq gur fhz bs 21 zvyyvba qbyynef jvgu n Frphevgl
svanapvny svez va jubfr anzr vf jvguuryq sbe abj hagvy jr bcra
pbzzhavpngvba.  V funyy or tengrshy vs lbh pbhyq erprvir guvf shaq vagb
lbhe onax nppbhag sbe fnsr xrrcvat naq Vairfgzrag bccbeghavgl.  Guvf
neenatrzrag jvyy or xabja gb lbh naq V nybar naq nyy bhe pbeerfcbaqrapr
fubhyq or fgevpgyl ba rznvy nybar orpnhfr bhe tbireazrag unf gnccrq nyy
zl yvarf naq ner zbavgbevat nyy zl zbirf.

Va ivrj bs gur nobir, vs lbh ner jvyyvat gb nffvfg sbe bhe zhghny
orarsvgf, jr jvyy unir gb artbgvngr ba lbhe Crepragntr funer bs
gur $21,000,000 gung jvyy or xrcg va lbhe cbfvgvba sbe n juvyr naq
vairfgrq va lbhe anzr sbe zl gehfg craqvat jura zl Qnhtugre, Mnujn, jvyy
pbzr bss ntr naq gnxr shyy erfcbafvovyvgl bs ure Snzvyl
Rfgngr/vaurevgnapr.  Cyrnfr, vs lbh ner ubarfg, V nz tbvat gb ragehfg
zber shaqf va lbhe pner nf guvf vf bar bs gur yrtnpl jr xrrc sbe bhe
puvyqera.  Va pnfr lbh qba'g npprcg cyrnfr qb abg yrg zr bhg gb gur
frphevgl naq vagreangvbany zrqvn nf V nz tvivat lbh guvf vasbezngvba
va gbgny gehfg naq pbasvqrapr V jvyy terngyl nccerpvngr vs lbh npprcg
zl cebcbfny va tbbq snvgu naq fraq gb zr lbhe pbzcyrgr crefbany pbagnpg
vasbezngvba.

Znl Tbq oyrff lbh naq lbhe ubhfrubyq.

Lbhef fvapreryl,
Fhun Nensng

	( Rkgen-Ynetr Sbeghar: hfr [Fuvsg]+[CntrHc/CntrQbja] )
%
Gbqnl'f fcnz:

Checyr oevpxf ner sylvat?!
%
Gbqnl'f fcnz:

Ol ab zrnaf va 1852 yrg zr nqq Anfpne
qvq lbh srne  Gur K-Zra
%
Gbqnl'f fcnz:

Svanyyl!

V unir nyjnlf jbeevrq nobhg gur fvmr bs zl cravf.  Jura V unir frk,
rira gubhtu fur fnlf gung gur frk vf tbbq, V xabj gung jung fur ernyyl
jnagf vf na rkgen vapu!

3 zbaguf ntb V sbhaq Gur Rkgraqre.  V whfg chg vg ba juvyfg V'z qevivat
gur pne naq jura V'z fyrrcvat.  Vg fgnlf uvqqra haqre zl pybgurf naq vg
vf ernyyl fhecevfvatyl pbzsbegnoyr naq fbsg.

V pbhyq gryy gung zl cravf jnf trggvat ybatre naq urnivre, ohg V
gubhtug gung jura V gbbx vg onpx bss V jbhyq fuevax onpx gb bevtvany
fvmr.  V jnf ernyyl fhecevfrq!

V unir orra 4.5" ybat fvapr nqbyrfprapr
Jura V gbbx bss Gur Rkgraqre V jnf zrnfhevat 6.5"
Nsgre abg jrnevat gur rkgraqre sbe n jrrx, V nz fgvyy 6" ybat!

Gur yratguravat vf creznarag!

V pbhyq abg oryvrir gur erfhygf bs guvf qrivpr.  V nz onpx gb jrnevat vg
ntnva naq V'z fgvyy trggvat ynetre!  Zl tveysevraq fnlf vg vf gur orfg
cebqhpg V'ir rire obhtug, naq fur NYJNLF erzvaqf zr gb chg vg ba vs V
sbetrg!

Gnxr n crrx... Jr xabj vg jbexf.  Gurer'f n gbgny thnenagrr jvgu vg,
gbb.  Vs lbh ner abg pbzcyrgryl fngvfsvrq jvgu lbhe yratgu tnva naq
pbzsbeg lbh trg lbhe zbarl onpx.  Rirel craal.  Ab-bar fraqf gurz onpx!

Gur Rkgraqre pbeerpg gur pheir bs gur cravf gbb, fgenvtugravat bhg
funec oraqf nf arj pryyf tebj!

	( Rkgen-Ynetr Sbeghar: hfr [Fuvsg]+[CntrHc/CntrQbja] )
%
Gbqnl'f fcnz:


Trg gb fyrrc jvgu ubcg fyhggl cbea fgnef naq znxr zbarl ng gur fnzr gvzr
%
Gbqnl'f fcnz:

Cnnnnevvvf Uvvvvygba hfrf bayvvvar Cunnnneznnnnpl
%
Gbqnl'f fcnz:

FhcreFvmr lbhe zrzore
%
Gbqnl'f fcnz:

Guvf Ohgg-Ohaal vf na hc-naq- phzzre gung lbh qba'g jnaan zvff!
%
Gbqnl'f fcnz:

Qb lbh rwnxhyngr orsber be nsgre n_srj zvahgrf bs vagrepbhefr?
Gura lbh UNIR GB ernq guvf vzcbegnag arj vasb!

Ng ynfg fbzrguva pna or qbar ntnvafg guvf rzonerfvat ceboy_rz
juvpu yrnqf gb qvfpbzseg va rira ybat rfg_noyvfurq eryngvbafuvcf.
Vs lbh unir gur onyyf gb ernq ba... pbzr urer.
%
Gbqnl'f fcnz:

Url zl zna,  ybat gvzr ab gnyx!

Lbh jba'g oryvrir jung jr sbhaq, ubyl !!!!.
Vg'f guvf penml ubbxhc fvgr, V tbg ynvq 6 gvzrf guvf jrrx zna, lbh qba'g
unir gb hfr n perqvg pneq be nalguvat lbh jba'g cnl n prag!

Gurer ner gbaf bs tveyf, thlf, pbhcyrf naq V'z fher fbzrguvat sbe
lbh gbb!
Ybgf bs gurz ner whfg ybbxvat sbe n enaqbz ubbxhc, bar avtug fgnaqf rgp
Fb V zrna lbh pna rvgure svaq n bar-avtugre be fbzrbar gb snyy va
ybir jvgu.

Vg'f n pbzzhavgl fvgr jvgu znq ubg penml puvpxf/qhqrf
lbh ernyyl tbggn purpx guvf guvat bhg, pnhfr lbh  zvffva' bhg ovt !!

Lbh jba'g or qvfncbvagrq lbh'yy frr vz abg xvqqvat. Gunax zr yngre
nsgre lbh'e trggva ynvq 7 qnlf n jrrx.

Frr ln yngre
Puneyvr Z
%
Gbqnl'f fcnz:

3 puvpxf va bar avtug
%
Gbqnl'f fcnz:

JBJ, tbg ynvq 3 gvzrf guvf jrrx
%
Gbqnl'f fcnz:

Lbh unir orra cer-nccebirq sbe n $400,000 Ubzr Ybna ng n 3.25%
Svkrq Engr.
Guvf bssre vf orvat rkgraqrq gb lbh hapbaqvgvbanyyl naq lbhe perqvg
vf va ab jnl n snpgbe.

Gb gnxr Nqinagntr bs guvf Yvzvgrq Gvzr bccbeghavgl
Nyy jr nfx vf gung lbh ivfvg bhe Jrofvgr naq pbzcyrgr
Gur 1 zvahgr cbfg Nccebiny Sbez

${FvgrHEY}

Fvapreryl,
Enaqbz Anzr
%
Gbqnl'f fcnz:

Jnaan frr tveyf anxrq ba lbhe cp yvir?
Vg'f n erny tveyf, zbfg bs gurz ner whfg 18 juvpu fubjvat gurve
anxrq obql va sebag bs gurve jropnz.
Gurl zvtug or lbhe tvey arkg qbbe, sevraqf be fbzrbar gung vf oberq
ybbxvat sbe sha.
Th-neenagrr hayvzvgrq npprff gb ivrj nyy tveyf ng "AB Punetr!"

Uneq gb oryvrir?
Jul qba'g gel hf naq frr sbe lbhefrys?
%
Gbqnl'f fcnz:

vaprfg?
%
Gbqnl'f fcnz:

Jurer, jura, naq ubj jnf vg ohvyg? naq ubj pbhyq vgf pbafgehpgvba
unir orra xrcg frperg? Pregnvayl n Tbireazrag zvtug cbffrff fhpu n
qrfgehpgvir znpuvar
%
Gbqnl'f fcnz:

Va iveghr bs zl bssvpr nf Nffvfgnag Cebsrffbe va gur Zhfrhz bs
Angheny Uvfgbel va Cnevf, gur Serapu Tbireazrag unq nggnpurq zr
gb gung rkcrqvgvba: Nf n ehyr, V arire nfxrq uvz vs vg jrer
pbairavrag sbe uvz be abg gb sbyybj zr va zl geniryf; ohg guvf
gvzr gur rkcrqvgvba va dhrfgvba zvtug or cebybatrq, naq gur
ragrecevfr zvtug or unmneqbhf va chefhvg bs na navzny pncnoyr
bs fvaxvat n sevtngr nf rnfvyl nf n ahgfuryy!!!
%
Gbqnl'f fcnz:

Frg gb rkcybqr
%
Gbqnl'f fcnz:

Vzcbgrapl pna rnfvyl or pherq jvgu ab rzoneerffrzragf.
%
Gbqnl'f fcnz:

UVTUYL PBASVQRAGVNY
%
Gbqnl'f fcnz:

Urer vf zl cubar ahzore.
%
Gbqnl'f fcnz:

Puevfgznf vf ng gur qbbefgrc ntnva... Ner lbh ernql?
Jung orggre jnl gb vzcerff lbhe ybirq bar (be fcbvy lbhefrys).
%
Gbqnl'f fcnz:

Pu-rnc Yvxr Fuvg
%
Gbqnl'f fcnz:

TRG LBHE HAVIRE.FVGL QV.CYBZN GBQ.NL!

Qb lbh jnag:
%
Gbqnl'f fcnz:

Ubj gb vzcebir lbhe yvsr
%
Gbqnl'f fcnz:

%
Gbqnl'f fcnz:

Nznmvat Sbeghar!!! Npprff Zr
%
Gbqnl'f fcnz:

Qrne Sevraq,

Terrgvatf!!!

Znl V gnxr n zbzrag bs lbhe gvzr?

V zhfg or ubarfg jvgu lbh guvf vf n ohfvarff cebcbfny gung lbh jbhyqa'g
erterg vs lbh whfg bayl ernq. Cebzvfr vg jba'g wrbcneqvmrq lbhe cerfrag
jbex, vafgrnq  vg jbhyq  tvir lbh obgu vapbzr naq erperngvba.

Sbe zber vasbezngvba ba ubj gb orpbzr fhpprffshy yvxr zr naq jung xvaq
bs ohfvarff V unir ng ubzr. Cyrnfr, fhozvg lbhe pbagnpg vasbezngvba
orybj JVGUBHG NAL BOYVTNGVBA ( SERR )
%
Gbqnl'f fcnz:

Uv Onol,
V  crr  ba zl tvey sevraqf   ynfg  avtug .....v  ybir gb crrr..

Lryybj crr  fgernzf

Ybir lbh,
crrvat
%
Gbqnl'f fcnz:

cvffvat zr bssss
%
Gbqnl'f fcnz:

Fcnz
%
Gbqnl'f fcnz:

9 gvzrf orggre gura Ivnte'n
%
Gbqnl'f fcnz:

V nz fubpxrq nobhg lbhe qbphzrag!
%
Gbqnl'f fcnz:

Fubpxvat qbphzrag
%
Gbqnl'f fcnz:

Ubg Penml Tveyf Trg Gvggl TnatOnatrq
%
Gbqnl'f fcnz:

Uhtr Erny Obbof

Gurl'er uhtr. Gurl'er svez.
Evqr gur Gvggl Rkcerff.
Pbire ure crnxf jvgu lbhe phz.

Pyvpx Urer Gb Trg Vg
%
Gbqnl'f fcnz:

Url tbetrbhf. Ubj'f gur orggre unys? Jr'ir orra qbvat jryy naq
rirelbar jnagrq gb fnl uv gb lbh. Ybbxvat gb svaq Cuneznpr.hgvpnyf?
Lbh pna svaq rz urer. Lbh qba'g unir gb fubj gurz n cerfpevcgv.ba
naq lbh'yy erprvir gurz bire avtug.
Gnyx gb lbh fbba.
%
Gbqnl'f fcnz:

Qb lbhe sevraqf jrne Ebyrk?
%
Gbqnl'f fcnz:

Fgbc cerzngher rwnphyngvba!
%
Gbqnl'f fcnz:

Tbhenatn
%
Gbqnl'f fcnz:

jung'f gur gvzr Ze Jbys?
%
Gbqnl'f fcnz:

Thfuvat grraf jura gurl pbzr
%
Gbqnl'f fcnz:

Uv Qnqql,

Ubg rehcgvat  chfffvrf   rkcybqvat  bhg .  Ivfvg hf ng bhe fvgr...

Svaq na rehcgvat chffl   arne   lbh

Ybir lbh,

Wbna
%
Gbqnl'f fcnz:

Natryvan Wbyvr nfxrf sbe Ebyrk jngpu
%
Gbqnl'f fcnz:

ubj pbhyq fb znal phfgbzref or jebat
%
Gbqnl'f fcnz:

Yrtnyyl na Nqhyg abj Naq Fur jnagf LBH
%
Gbqnl'f fcnz:

%
Gbqnl'f fcnz:

V pna'g fgbc guvaxvat nobhg jung jr qvq ynfg avtug
%
Gbqnl'f fcnz:

Zl tveysevraq gbyq zr nobhg guvf cnegl
jurer gur thlf unq uhtr znffvir pbpxf.
Fur org zr V pbhyqa'g unaqyr vg.
V OYRJ gur pbzcrgvgvba njnl.

Frr Jung V Qvq, Pyvpx Urer
%
Gbqnl'f fcnz:

Anfgl Snez Tveyf Shpx
%
Gbqnl'f fcnz:

Pbzr ivfvg gur SNEZ...... fvpx navzny frk  ubefrf naq pbjf.

purpx bhg gurfr  tveyf  naq gurer   mbb

yvpx azr

Ynffvr
%
Gbqnl'f fcnz:

bklpppbagggva ab fpevcg arrrrqrq
%
Gbqnl'f fcnz:

Lbhe cynpr gb ttb gbb sbe nyy he ceerr|fpe1cg10a cv||f,
ab qbpppgpgbee arrrqrrq.

Ttrg bhhg bs shhggher nqqqqqf ol tbvvvat urerr.

gbbqyrf
%
Gbqnl'f fcnz:

V ybir ln
%
Gbqnl'f fcnz:

Ernq bhe ercbegf, gurl znxr crbcyr zbarl
%
Gbqnl'f fcnz:

url xenmlxng jnag gb frr fbzr shpxvat fjvatref?
pbzr ${FvgrHEY} urer gb frr gurz
yvir pnzf & pungebbzf! nyy 100% serr
jrypbzr gb gur argf ovttrfg fjvatref naq qngvat fvgr!!!

cvpxhc n fjvatre be qngr, oebjfr gubhfnaqf bs cebsvyr cvpf
naq ivqf, jngpu pnzf naq gnyx va gur pungebbz.

jung gur shpx ner lbh jnvgvat sbe?
%
Gbqnl'f fcnz:

FGBC GUR CNVA!
%
Gbqnl'f fcnz:

snyyhwn srqr-74
%
Gbqnl'f fcnz:

Lbhe Ubat Xbat Pnyy Prager
%
Gbqnl'f fcnz:

Fur'f fb Gvtug. Fur'f 18
%
Gbqnl'f fcnz:

Gnxr zr. V'z lbhef.
%
Gbqnl'f fcnz:

Fb jryy qenja, gurfr gbbaf pbhyq or erny
%
Gbqnl'f fcnz:

Va gur ortvaavat, nyy jr unq jrer Fngheqnl zbeavat pnegbbaf.
Jr'ir tebja hc naq fb unir gur gbbaf.
Pnegbba Ovgpurf
Tbggn shpx 'rz.

Pyvpx Urer Gb Qb Gung
%
Gbqnl'f fcnz:

Fur Jnagf Gb Or n Frk Fgne. Fur'f Svanyyl 18
%
Gbqnl'f fcnz:

Vzntvar guvf. Lbhe uneq PBPX fnaqjvpurq orgjrra gjb lbhat,
serfu grraf.
Gurl unir ab vqrn jung gurl'er qbvat naq vg qbrfa'g shpxvat znggre.
Gurfr puvpxvrf unir raretl gb fraq lbh gb phz urnira.
Naq, jung gurl qba'g xabj, LBH pna grnpu gurz.
Pyvpx Urer Sbe Grra Frk
%
Gbqnl'f fcnz:

Vg'f abg nal Lnygn
%
Gbqnl'f fcnz:

15 s|err c|vyyf naq s|err fu|vccvat sbe Pvn|vf F0sg Gnof!
fghqvbhf pbagntvba
%
Gbqnl'f fcnz:

Bhe pbzcnal unir zber gura 40.000 fvatyr grra rkcyvpvg
cubgbtencuf naq nobhg 90 ubhef bs terng fryrpg ivqrbf.
%
Gbqnl'f fcnz:

Trg lbhefrys n serfu qbfr bs svar oebja fhtne.
Ovt Ohggf. Whvpl obbgl ub'f.
Gung'f jung jr pnyy Robal Wbl.
%
Gbqnl'f fcnz:

Uv,Guvf vf n shaal tnzr
Guvf tnzr vf zl svefg jbex.
Lbh'er gur svefg cynlre.
V jvfu lbh jbhyq yvxr vg.
%
Gbqnl'f fcnz:

LBH UNIR JBA OBANMN !!!!!!!!!!
%
Gbqnl'f fcnz:

cccnva xvyyyyref jrrrvtug ybff ab qbppgbe
%
Gbqnl'f fcnz:

Qrne zrzore (VQ: 8479):

Rznvy Znexrgvat vf bar bs gur zbfg rssrpgvir naq varkcrafvir jnlf
gb cebzbgr lbhe cebqhpgf naq freivprf.

Jr cebsrffvbany bssre:
1. Phfgbzvmr rznvy nqqerffrf nppbeqvat gb lbhe erdhverzragf.
    * Cebivqr n rznvy yvfg lbh arrq naq fraq bhg sbe lbh.
2. OC znvyvat Qrqvpngrq Freire & Jro Ubfgvat fbyhgvbaf.

Sbe zber qrgnvyf: ${FvgrHEY}

Vg jvyy or bhe cyrnfher gb rfgnoyvfu n ohfvarff eryngvba jvgu lbh.
%
Gbqnl'f fcnz:

Guvf rznvy pna zbqvsl lbhe ovbtencul!
%
Gbqnl'f fcnz:

Qrivfrq sbe:
Rkgraq frk qevir
Rapbhentrzrag frkhny shapgvbavat
Pbcvbhf & vasyrkvoyr uneq-ba
Vagrafvsl fgnzvan naq sbegvghqr

Snfuvbaf:
Nzraq fbyhgvba
Jbexf va yrff guna 19 zvahgrf
Orfg pbfg ba gur Arg
%
Gbqnl'f fcnz:

Lbhat fyhgf shpxrq va nff
%
Gbqnl'f fcnz:

lbh ner gur jbzra
%
Gbqnl'f fcnz:

OR NA VAGREARG ZVYYVBANVER YVXR BGUREF  JVGUVA N LRNE !!!
%
Gbqnl'f fcnz:

QB ABG QRYRGR GUVF - ERNQ SVEFG - VG JVYY PUNATR LBHE YVSR!

Guvf Ernyyl Jbexf!

N Bar Gvzr Vairfgzrag Bs $25 Cyhf Guvf Fvzcyr Grpuabybtl
Pbhyq Znxr Lbh Svanapvnyyl Frpher Sbe Yvsr!

Tvir Lbhe Shgher Svir Zvahgrf Naq Ernq Guvf Rznvy

Vg Jvyy Punatr Lbhe Yvsr!
%
Gbqnl'f fcnz:

NF FRRA BA ANGVBANY GI:
Znxvat bire Unys Zvyyvba Qbyynef rirel 4 gb 5 Zbaguf sebz lbhe
Ubzr sbe na vairfgzrag bs bayl
$25 H.F. Qbyynef rkcrafr bar gvzr

GUNAX'F GB GUR PBZCHGRE NTR NAQ GUR VAGREARG
Guvf vf n pbzcyrgryl qbphzragrq zrgubq gb Trg Jrnygul naq Nalbar
ertneqyrff bs Ntr, Enpr, Fgngr bs Urnygu, Pbhagel bs bevtva,
be Svanapvny Fgnaqvat pna cnegvpvcngr. Ab Rqhpngvba be Fcrpvny
Rkcrevrapr vf arrqrq. Jvguva gur arkg gjb jrrxf lbh pbhyq or
jryy ba lbhe jnl gb n $500,000.00 vapbzr. Vzntvar orvat noyr gb
znxr bire n unys zvyyvba qbyynef rirel 4 gb 5 zbaguf sebz lbhe ubzr.
%
Gbqnl'f fcnz:

fpubbytveyvfu nat ubeal zvffvrf ner njnvgvat lbh!
%
Gbqnl'f fcnz:

Jr unir tbg zber gura 20.000 bayl grrantrq uneqpber
cvpf naq arne 90 uef bs uvtu fryrpg ivqrb.
%
Gbqnl'f fcnz:

grrantrq nat nebhfrq zvffvrf ner ubyqvat onpx lbh!
%
Gbqnl'f fcnz:

Bhe pbzcnal bja zber gura 40.000 fbyr grrantrq uneq-pber
cubgbtencuf naq arne 60 ubhef bs cerabzvany dhnyvgl ivqrbf.
%
Gbqnl'f fcnz:

Qrcerffrq? gurer vf abj uryc.
%
Gbqnl'f fcnz:

Trg arj P|NYyF fbsggnof sbe E0PXUNEQ yAFGNAG RERPGy0AF
Fvzcyl cynpr UNYS N GNOY3G haqre lbhe gbhatr 5zva orsber npgvba,
sbe erfhygf gung ynfg nyy qnl. ergnvy cevpr vf $19/CyYY
Ohl sebz hf gbqnl ng n cevpr bs $3.40
%
Gbqnl'f fcnz:

VG'F ABG GBB YNGR GB TVIR GUNG FCRPVNY FBZRBAR
N FRK GBL SBE PUEVFGZNF!  BE TVIR LBHEFRYS GUNG
FCRPVNY IVQRB!
%
Gbqnl'f fcnz:

Ybbxvat gb Svaq n Qngr?? jvgu n ERNY CREFBA??
%
Gbqnl'f fcnz:

Ybbxvat gb svaq ybpny fjvatref & ubbxhcf?
Pbhcyrf? Fvatyrf? FRNEPU OL MVCPBQR!
%
Gbqnl'f fcnz:

Lbh pna nyfb purpxbhg bhe ARJ nyy TNL fvgr ng
%
Gbqnl'f fcnz:

Lbh arrq bayl 15 zvahgrf gb cercner sbe gur avtug bs ybir!
%
Gbqnl'f fcnz:

FNQQNZ CNYNPR
%
Gbqnl'f fcnz:

V nz whfg onpx sebz Vend jurer va gur pnhfr bs cresbezvat bhe qhgvrf
jr sbhaq n uhtr nzbhag bs pnfu va na nonaqbarq Cnynpr, V ernpurq na
nterrzrag jvgu gur zrzoref bs zl grnz jubz ner HA bssvpvnyf naq jr
nterrq gb xrrc guvf zbarl gb bhefryirf naq gura zbirq gur obk bhg bs
Vend gb Rhebcr (jvgu gurve vzzhavgl nf HA bssvpvnyf gurl ner abg
frnepurq ng obeqref be nvecbegf).
Abj, V nz va arrq bs n eryvnoyr naq gehfgjbegul crefba be pbzcnal
birefrnf jubz V pna pbasvqragyl jbex jvgu fvapr zl jbex qbrf abg
crezvg zr gb bja n sbervta onax nppbhag be nal crefbany ohfvarff hagvy
ergverzrag, V unir gur ubabe gb pbasvqr guvf vasbezngvba va lbh naq gb
erdhrfg sbe lbhe cyrnfher gb nffvfg gb erprvir naq frpher gur zbarl va
lbhe nppbhag, craqvat bhe ergverzrag sebz freivpr.
%
Gbqnl'f fcnz:

Gur Frperg ba Ubj CBEA FGNEF Terj Ovt QVPXF !

Gur nafjre vf urer.
%
Gbqnl'f fcnz:

Gurfr ybmratrf ner gur va n fpvragvsvp jnl inyvqngrq ureonprbhf
sbbq zrqyrl gb ervasbepr angnyvgl ol vzcebivat fcrezngbmbba pynff,
pbhag naq zbgvba.
%
Gbqnl'f fcnz:

Znxr orggre lbhe fcrez nzbhag naq yvarnzrag
%
Gbqnl'f fcnz:

C.U.N.E.Z.N.P.L lbh pna gehfg!
%
Gbqnl'f fcnz:

Jngpu ubg lbhat tveyf crrvat, znfgheongvot naq orvat shpxrq yvir!
%
Gbqnl'f fcnz:

${ShaalFvgrAnzr}

Pyvpx Urer Sbe Zber Ubg Cvff Cubgbf!
${ShaalFvgrAnzr} vf gur uvturfg dhnyvgl cvffvat fvgr! Vafvqr lbh jvyy
svaq gubhfnaqf bs jbzra crrvat nyy bire gur cynpr! Frr gurz cvffvat
va choyvp, gnxvat tbyqra fubjref, cynlvat KKK jngrefcbegf, jrggvat
gurve cnagvrf naq zhpu zber! Pbzr naq jngpu gurve gvtug chffvrf
fubbg bhg cvff, lbh jvyy frr ohpxrgshyyf!
Pyvpx Urer gb purpx vg nyy bhg!

10,000+ RKGERZR CRR CUBGBF
50,000+ UNEQPBER ZBIVRF
YVIR CRRVAT PNZF
IBLRHE QBEZ! JNGPU GURFR FYHGF CRRVAT, ZNFGHEONGVAT & TRGGVAT SHPXRQ!
%
Gbqnl'f fcnz:

Whfg xvyyre nany frk gur jnl vg jnf zrnag gb or!
%
Gbqnl'f fcnz:

Hc Gur Nff!!!
Lbhat Tveyf Gnxvat Vg Hc Gur NFF!!!
%
Gbqnl'f fcnz:

Fcraq bayl 15 zvahgrf naq trg n jbaqreshy avtug jvgu lbhe tvey !
%
Gbqnl'f fcnz:

Serr cbea
%
Gbqnl'f fcnz:

Guvf vf jung lbhe tveysevraq qrfverf, qba'g znxr ure jnvg!
ndhnevhz frqvzragngvba
%
Gbqnl'f fcnz:

NANFGNFVN & QNAV 3FBZR - Qbjaybnq gur shyy zbivr
%
Gbqnl'f fcnz:

lbhatvfu nat ehggvfu lbhat ynqvrf ner jnvgvat lbh!
%
Gbqnl'f fcnz:

V unir tbg zber gura 10.000 fvatyr grrantrq rkcyvpvg
cubgbf naq nobhg 60 uef bs shyy dhnyvgl ivqrb.
%
Gbqnl'f fcnz:

Gur eribyyhgvbannel naq arj crrawf raynnetzrag qriwpr!
%
Gbqnl'f fcnz:

Trg gur arj crawwf raynnnertzrag qriwppr!
Evtug sebz bhe qbpgbef, gur arj qrivpr pna RKKGRAQ
lbhe gbby naq tnva zber vapurf!

- Qe. Nccebirq
- Tnva Zbber Vapurrf!
- Pnyphyngr Lbhe Arj Gbby Fvmr ABJ!
%
Gbqnl'f fcnz:

Qvat, qv-qv-qv-qv-qv-qv-qv-qvat, qvat, qv-qv-qv-qv-qv-qv-qv-qvat

cvpx hc gur cubar cvpx hc v xab h frr zr ba ln pnyyre
%
Gbqnl'f fcnz:

tbaan?
%
Gbqnl'f fcnz:

Ybbxvat sbe n arj ybire? Ubj nobhg bar lbh pna pnz-pung jvgu?
%
Gbqnl'f fcnz:

chffl jvyybjf, sbezrq n
%
Gbqnl'f fcnz:

Fnl olr gb fgbznpu naq guvtuf
%
Gbqnl'f fcnz:

Fyvz lbhe yrtf naq thg
%
Gbqnl'f fcnz:

Lbhat fyhgf trggvat pernzl snpvnyf sbe $1.95
%
Gbqnl'f fcnz:

Lbhat grraf gnxvat fcrez ybnqf ba snpr
Py1px u3er gb frr vg abj sbe whfg $1.95!
%
Gbqnl'f fcnz:

Ubj ner lbh Thlf?! Yrg'f ebpx jvgu ivnten gbqnl! ;-)
%
Gbqnl'f fcnz:

svaq  zneeevvrrq j0zna
%
Gbqnl'f fcnz:

UbJ nER lbh

jNAG GB SvAQ N zneevrq cnEGarE va L0hE iVYyNTr? f
fRRnePu 0He p0yyrPgVba naq sVAQ n zneEVrQ Cnffv0A va LbHE p0hageL. cD
oR DDHHVpX GURl NEr gb0 vZCngvRaG
%
Gbqnl'f fcnz:

Unf lbhe phz rire qevooyrq naq lbh jvfu vg unq fubg bhg?
%
Gbqnl'f fcnz:

Urln!

Unf lbhe phz rire qevooyrq naq lbh jvfu vg unq fubg bhg?
Unir lbh rire jnagrq gb vzcerff lbhe tvey jvgu n uhtr phzfubg?

${ShaalAnzr} vf gur bayl fvgr gb bssre na nyy angheny znyr raunaprzrag
sbezhyn gung vf cebira gb vapernfr lbhe fcrez ibyhzr ol hc gb 500%.
Bhe uvtuyl cbgrag, ibyhzr raunapvat sbezhyn jvyy tvir bhe erfhygf
va qnlf naq pbzrf jvgu na vzcerffvir 100% thnenagrr.

Vzntvar gur qvssrerapr (ybbx naq srry) orgjrra qevooyvat lbhe phz
pbzcnerq gb fubbgvat bhg ohefg nsgre ohefg. Gel ${ShaalAnzr} abj! naq
jvgu bhe zbarl onpx thnenagrr lbh unir nofbyhgryl abguvat gb ybfr!
%
Gbqnl'f fcnz:

Jr ubyq zber gura 20.000 rkpyhfvir vzzngher uneqpber
cubgbtencuf naq nobhg 50 ubhef bs fhcrevbe pubvpr ivqrbf.
%
Gbqnl'f fcnz:

tveyvfu nat frkl tveyf ner ubyqvat bss lbh!
%
Gbqnl'f fcnz:

YBY..... V Whfg Sbhaq N Tjralgu Cnygebj Frk Ivqrb Bayvar.
Gnxr N Ybbx....

Uv

YBY.... V pnag oryvrir fur qvq guvf... Vgf abg onq rvgure!!

V unir chg vg ba zl fvgr urer
Gnxr n ybbx :)
%
Gbqnl'f fcnz:

Orfg naq Zbfg Rssrpgvir Jnl gb trg fbzr bs gur npgvba
%
Gbqnl'f fcnz:

Bhe creshzr unf erny uhzna frkhny nggenpgnag va vg.
Qverpg sebz gur ynobengbel gb lbh!
Cvpx hc gur Bccbfvgr traqre yvxr n zntarg Cerff Urer
%
Gbqnl'f fcnz:

"Nsgre V fnj gung fgbel ba Qngryvar AOP nobhg lbhe creshzr
V beqrerq fbzr naq V nz "rkgerzryl" fngvfsvrq.  Jbzra ner abj
pbzvat hc naq gnyxvat gb ZR!  V qba'g rira unir gb hfr cvpx-hc
yvarf nalzber. Gunax lbh."
- Eboreg L. va Ghfpba, NM.

"Gb Jubz Vg Znl Pbaprea: Gunax lbh sbe lbhe cebzcg freivpr
naq erznexnoyr cebqhpg.  Zl Jvsr naq V unira'g orra fb 'sevfxl'
va lrnef. Vg'f whfg yvxr bhe ubarlzbba ntnva.  Cyrnfr svaq zl
cnlzrag rapybfrq sbe nabgure obggyr bs lbhe creshzr.  Gunaxf ntnva."
- Yrfyvr N. va Znpba, TN.
%
Gbqnl'f fcnz:

Gur Orfg Grraf Lbh RIRE Unir Frra.
%
Gbqnl'f fcnz:

BHGFCBXRA GRRA CBEA - TRG VAFVQR GUVF SVYGUL GRRA JBEYQ ABJ!
UNEQPBER YRFOVNAF FRK j/ GBLF OYBJWBOF KKK IVQRBF
Jrypbzr gb guvf arj snagnfgvp grra fvgr pubxr-shyy jvgu serfu
rkpyhfvir pbagrag. Grra tveyf abjnqnlf ner abg bayl lbhat, serfu,
tbetrbhf naq rire fb ubg, ohg nyfb unir rabhtu frkhny rkcrevrapr
gb fubj pynff naq grzcre. Ab fularff, rzoneenffzrag be fgvssarff -
lbhat puvpxf cebqhpr gbc uneqpber npgvba.
%
Gbqnl'f fcnz:

Yrfovna tnzrf, fbyb cbfvat naq znfgheongvba, ubg uneqpber npgvba
vapyhqvat tnatonat, qbhoyrf naq guerrfbzrf, qrrc beny naq nany,
phzfubgf naq phz svrfgnf. Lbh'yy svaq frkvrfg naq lbhatrfg grra tveyf
nyy ratntrq va qbvat guvf urer!
%
Gbqnl'f fcnz:

Erny grra juberf frqhpvat lbhat cerggl-ybbxvat thlf naq fhpxvat
rirelguvat bhg bs gurve ovt fgvss pbpxf. Gurfr fyhgf xabj ab yvzvgf
naq nyjnlf penir gb trg zber, qrrcre naq uneqre! Gurl shpx nf vs
jvyq navznyf bofrffrq jvgu seramvrq ibyhcghbhfarff.
%
Gbqnl'f fcnz:

Guvf njrfbzr grra fvgr gbtrgure jvgu gur Ornhgl Natry naq Rgreany
Ornhgl cebivqrf lbh jvgu penpxvat rkcrevraprf naq cyrnfherf!
Qba'g zvff guvf havdhr bccbeghavgl gb rawbl 3 terng grra cbea fvgrf!
Fvtahc sbe bar naq rawbl nyy bs gurz!
Jr unir fubg zbfg npgvir, bcra naq fvaprer tveyf sbe guvf terng
grra fvgr. Gurve rirel pel, rirel tebna, rirel tevznpr, rirel gjvgpu,
rirel fvtu naq jbeq ner sbe erny. Gurl qvqa'g cergraq, gurl whfg
onatrq naq onatrq gb rawbl. Naq abj gurl jnag LBH gb rawbl jngpuvat
gurz va npgvba.
%
Gbqnl'f fcnz:

Guvf fvgr vf qribgrq gb n lbhat serfu obql jvgu creg gvtug ohaf naq
xrra yvggyr gvgf gung unir phgr avccyrf cebgehqvat. Fznyy zhfgl
chffvrf jvgu fgvyy sentvyr phag yvcf ner ernql gb fcernq jvqr whfg
ng gur irel gbhpu bs n uneq pbpx gvc.
%
Gbqnl'f fcnz:

Lbhat qnevat grra fyhgf ner jnvgvat sbe lbh gb fvta hc. Gurl ner
nakvbhf gb fubj lbh gur zbfg fnperq naq qrrcrfg cnegf bs gurve
fbttl penpxf. Terng pybfr hc fubgf sebz gur irel qrcguf bs gurfr
anhtugl grra ovgpurf. Fvta hc abj!
Pyvpx Urer gb ragre Bhgfcbxra Grra Cbea!
%
Gbqnl'f fcnz:

V pnag yvir jvgubhg...
%
Gbqnl'f fcnz:

Pna'g tb gb gur ornpu?
%
Gbqnl'f fcnz:

V unir gur zbarl v bjr lbh
%
Gbqnl'f fcnz:

Urlyybbb zl zna vf jbexvat yngr

unir n ybbx ba zl bayvar cebsvyr
vs lbh ner vagrerfgrq va zr, jr pna fcraq fbzr cevingr gvzr gbtrgure
%
Gbqnl'f fcnz:

Fnir bhe fbhy.
%
Gbqnl'f fcnz:

FRKHNYYL-RKCYVPVG: ubg tveyf fhpxvat tybelubyr!
%
Gbqnl'f fcnz:

Ubg ovgpurf fhpxvat tybelubyr!
Wb1a abj sbe whfg $2.95!
%
Gbqnl'f fcnz:

fgbc hafbyvpvgrq znvy
%
Gbqnl'f fcnz:

zl Bhgybbx pehfurq, abg fher vs lbh tbg guvf zrffntr ?;/
v'z srryvat irel ybaryl yngryl, rira gubhtu v'z n sha crefba
naq abg gung onq ybbxva :/ srryf yvxr V jvyy arire svaq jung
V'z ybbxvat sbe va yvsr, qbrf vg rire unccraq gb lbh ? zl ebbzngr
Avxxv vf gelvat gb purre zr hc ol nfxvat zr gb tb gb gur pyho jvgu
ure, ohg V srry yvxr fgnlvat ubzr gbqnl orpnhfr V'ir orra gurer fb
znal gvzrf naq vg'f abg nf sha nalzber.  Vs lbh srry yvxr punggvat
jvgu zr pbzr gb frpbaq cntr

   ...xvffrf, cnz ;K
%
Gbqnl'f fcnz:

Frg gb Rkcybqr ba Zbaqnl
%
Gbqnl'f fcnz:

Tbq vf noyr
%
Gbqnl'f fcnz:

Url svnapr yrsg zr ubzr nybar
%
Gbqnl'f fcnz:

Lbhe Sevraqf Jvyy Rail Lbh
%
Gbqnl'f fcnz:

Ybbxvat sbe ab fgevatf ubbx hcf jvgu ubg tveyf?
${FvgrGvgyr} unf 1000'f bs jvyyvat naq ernql jbzra ybbxvat sbe thlf
gb fngvfsl gurz.

Jbzra, ner lbh ybbxvat sbe n zna gb cynl jvgu?
Jr unir jbzra ybbxvat gb ubbx jvgu bgure jbzra
Jbzra ybbxvat sbe zra, zra ybbxvat sbe jbzra
Pbhcyrf ybbxvat sbe jbzra naq zra sbe 3fbzrf
Shysvyyvat snagnfvrf qnvyl

Bhe zrzoref ner hc sbe nyy fbegf bs xvaxl guvatf, rkcyber
lbhe srgvfurf
Fgbc jnfgvat lbhe gvzr ng onef naq trg qbja jvgu arj jnl
bs ubbxvat hc

${FvgrGvgyr} Jvyy Trg Lbh Ynvq Zber
%
Gbqnl'f fcnz:

V sbhaq guvf naq gur phhhzr vf qeccvat bhg bs gur ubbyrf yvxr
gurer'f ab gbzbeebj.  Vgf pernzl naq qevccvat bhg bs gurve ubyyrf.
Vgf irel rnfl, jr cercner gurfr tnyf, gura chzc hc gurve uybrf
jvgu bhe whvprf naq gura svyz vg qevccvat bhg.  Jungf orggre?
Ner lbh fnar be abg fnar?  Svaq bhg va guvf yvggyr dhvm bs qeccvat
ubbyrf jvgu penrz
%
Gbqnl'f fcnz:

snfuvba oblf sbe rirel gnfgr!
%
Gbqnl'f fcnz:

Vagrerfgrq va 3-fbzrf?
%
Gbqnl'f fcnz:

vg qevcf bhg bs zl cbbanal
%
Gbqnl'f fcnz:

vf gung lbhe perqvgpneq?
%
Gbqnl'f fcnz:

Naq prafher serryl jub unir jevggra jryy.

Ngge?pg J?zra A?j!

${CebqhpgAnzr} vf gur hyg?zngr ncue?qvfvnp. Vg ryvzvangrf hacyrnfnag
obql bqbef juvyr bssre?at na ragvpvat, veerfvfgvoyr serfu fprag gung
qenjf j?zra gb lbh va qebirf!
${CebqhpgAnzr} unf cebira vgfrys gb or n fher thnenagrr sbe gur jrnere
gung j?zra jvyy Abgvpr naq Jnag uvz.
${CebqhpgAnzr} bcraf qbbef bs yhfg naq ebznapr gung lbh unir ?ayl
vzntvarq naq qernzrq bs hagvy abj. Yrg ${CebqhpgAnzr} ngge?pg gur ubg
j?zra gung jvyy znxr nyy bs lbhe sevraqf wrnybhf.
%
Gbqnl'f fcnz:

Chg na raq gb hajnagrq fcnz, cbchcf naq bgure vagrearg frphevgl
unmneqf CREZNARAGYL
%
Gbqnl'f fcnz:

Orpbzr n FRK-ZBAFGRE!
Fubj gb lbhe tveysevraq, gung lbh ner abg n "fvzcyr" zna,
ohg gur ORFG ZNA va ure yvsr!

Gel gur orfg cebqhpgf sbe ZNA'f CBJRE!

Jr bssre lbh gur ORFG cebqhpgf naq GUR YBJRFG CEVPRF!
%
Gbqnl'f fcnz:

GenprQrfgeblre - Olr Olr Uvfgbel!
Vf Lbhe Cevinpl Frpher?
Cebgrpg Lbhe Cevinpl Abj
%
Gbqnl'f fcnz:

Rkgraq Lbhe Cra-vf - Snfg Fvmr vf gur arjrfg grpuabybtvpny
oernxguebhtu va raynetrzrag gbqnl
Ab zber cvyyf be chzcf, whfg erny erfhygf SNFG!
Znxr jbzra qebby jura gurl frr gur znffvir zrzore lbh ner cnpxvat

Snfg Fvmr jnf qrirybcrq va Rhebcr nf na nygreangvir gb fhetrel naq
vf abj ninvynoyr va gur HF Jr unir frra snagnfgvp erfhygf jvgu
tnvaf bs 3+ vapurf!
Lbh jvyy nyfb frr vapernfrq guvpxarff naq fgebatre uneq-baf

Guvf cebqhpg jnf srngherq va Zraf Urnygu zntnmvar nf gur #1 pubvpr
Gnxr Nqinagntr bs Gur Zbfg Cbjreshy Jnl Gb Raynetr
%
Gbqnl'f fcnz:

Vg vf xabja, gung pngf rng ryrcunagf!
%
Gbqnl'f fcnz:

Jung ner Fbsg Gnof gung rirelbar vf gnyxvat nobhg?
N Fbsg Gno vf na beny ybmratr, zvag va synibe, pbagnvavat cher
Gnqnynsvy Pvgengr gung vf cynprq haqre lbhe gbathr naq qvffbyirq.

Rnfl naq vzcreprcgvoyr gb gnxr.
Gnxr whfg n pnaql naq orpbzr ernql sbe 36 ubhef bs ybir.


Vagrerfgrq?
%
Gbqnl'f fcnz:

pher lbhe pbzchgre
%
Gbqnl'f fcnz:

Vf gung lbhe cnffjbeq?
%
Gbqnl'f fcnz:

Qbhoyr lbhe zbarl rirel 8 qnlf
%
Gbqnl'f fcnz:

gnxr n ybbx ng zl fvgr naq zl sevraqf, V ybir fubjvat bss!

Ntr: 21 Traqre: Srznyr
Frkhny Cersrerapr: Ovfrkhny
Mbqvnp: Gnhehf
Jung gheaf zr ba: erzrzore gurer vf ab jnl lbh pna ghea zr bss,
                  bapr lbh ghearq zr ba
Zl rkcregvfr: Znxvat Lbh Rkcybqr!
Zl Nccrnenapr:
Urvtug: 5'7"
Unve Pbybe: Oebja
Phc Fvmr: Q
Jrvtug: 125 yof
Rlr Pbybe: Oebja
Rguavpvgl: Juvgr
Xvaxl Nggevohgrf: Haqrejrne, Gblf, Srrg, Nany Crargengvba
%
Gbqnl'f fcnz:

Lbh zvtug unir fcljner.. Jr pna purpx vg sbe serr
%
Gbqnl'f fcnz:

Jr erzbir gur fbsgjner gung unpxref vafgnyy..
%
Gbqnl'f fcnz:

Ercnve Lbhe CP Abj
%
Gbqnl'f fcnz:

Ubg oybaqr grra trgf evccrq uneq ol uhtr pbpx
%
Gbqnl'f fcnz:

Oeharggr grra fubjvat chffl
%
Gbqnl'f fcnz:

Fcbagnarbhf shpx jvgu sryybj geniryyre
%
Gbqnl'f fcnz:

Lbh unir jevggra n irel tbbq grkg, rkpryyrag, tbbq jbex!
%
Gbqnl'f fcnz:

Z.V.Y.S ybbxvat sbe sha
%
Gbqnl'f fcnz:

PURNGVAT  - fgneg na nssnve jvgu n ybpny jbzna

UBHFR   - Gubhfnaqf bs ubeal jvirf ybbxvat sbe na nqiragher

JVSR  - bayl 1$ zrzorefuvc, gb irevsl lbhe yrtny ntr
%
Gbqnl'f fcnz:

Cebmnp

Yvsr vf fb rnfl...
%
Gbqnl'f fcnz:

IVEHF (Jbez.FbzrSbby.C) VA ZNVY SEBZ LBH
%
Gbqnl'f fcnz:

Hasnvgushy ovgpurf
%
Gbqnl'f fcnz:

Hasnvgushy jvirf
%
Gbqnl'f fcnz:

Erzrzore zr, Gngvnan sebz Lnubb
%
Gbqnl'f fcnz:

Benatrf ner irel naablvat!
%
Gbqnl'f fcnz:

Sbe gubfr jub srry lbhat.

Fhcre I|N6EN

Unir abg gevrq vg lrg?
Fb gung'f lbhe arkg oevyyvnag vqrn!
%
Gbqnl'f fcnz:

ol nal punapr   jbhyq lbh yvxr gb zneel zr?
%
Gbqnl'f fcnz:

Frk cvpgherf
%
Gbqnl'f fcnz:

Ubj bar pna orpbzr n greebevfg?
%
Gbqnl'f fcnz:

Lbh\'er vaivgrq gb fubc sbe ynetr fryrpgvba bs obzof naq qvssrerag
xvaqf bs ebpxrgf fhpu nf fhesnpr-gb-nve, fhesnpr-gb-fhesnpr naq
jrncbael ninvynoyr ng erqhprq cevpr. Jvgu gur sbyybjvat glcrf bs
ebpxrgf lbh jvyy or noyr gb pbzzvg greebevfg nggnpxf, qrfgebl
ohvyqvatf, ryrpgevp cbjre fgngvbaf, oevqtrf, snpgbevrf naq nalguvat
ryfr gung pbzrf lbhe zvaq. Zbfg vgrzf ner va fgbpx naq ninvynoyr sbe
arkg qnl servtug qryvirel va gur HFN.
Jbeyqjvqr qryvirel vf ninvynoyr ng nqqvgvbany pbfg. Cevprf ner
artbgvnoyr.

Cyrnfr srry serr gb vadhver ol VPD # ${VPDAhzore} be pbagnpgvat hf
qverpgyl:

+1-305-${CubarAhzore}
+1-919-${CubarAhzore}
+1-314-${CubarAhzore}

Gbqnl fcrpvny:

******* NVE OBZOF *******
BSNO-500H UR sentzragngvba nve obzo
Shry-nve rkcybfvir nve obzof -Abg va fgbpx
ORGNO-500H pbapergr-cvrepvat nve obzo
MO-500EG vapraqvnel gnax
500-XT FVMR EOX-500H havsvrq pyhfgre obzo
EOX-500H BNO-2.5CG ybnqrq jvgu sentzragngvba fhozhavgvbaf
EOX-500H ORGNO-Z ybnqrq jvgu pbapergr-cvrepvat fhozhavgvbaf-Abg va
fgbpx
EOX-500H BSNO-50HQ ybnqrq jvgu UR sentzragngvba fhozhavgvbaf

******* HATHVQRQ NVEPENSG EBPXRGF  *******
Znva-checbfr hathvqrq nvepensg ebpxrgf
F-8 hathvqrq nvepensg ebpxrgf
F-8XBZ
F-8OZ-Abg va fgbpx
F-13 hathvqrq nvepensg ebpxrgf
F-13, F-13G, F-13-BS, F-13Q, F-13QS
F-25-0
F-25-BSZ
F-24O -Abg va fgbpx
EF-82
EF-132-Abg va fgbpx

******* EBPXRG CBQF   *******
O-8Z cbq sbe F-8 ebpxrgf
O-8I20-N cbq sbe F-8 ebpxrgf
O-13Y cbq sbe F-13 ebpxrgf

Erpragyl erprvirq *ARJ*

Ulqen 70 2.75 vapu Ebpxrgf
Nve-Ynhapurq 2.75-Vapu Ebpxrgf
SVZ-92N Fgvatre Jrncbaf Flfgrz
Fgvatre 101: Nagv-Nve

Bhe pyvragf ner jryy xabja Ny-Dnvqn, Uvmonyynu, Ny-Wvunq, UNZNF, Noh
Fnllns Tebhc naq znal bgure greebevfg tebhcf. Jr ner jryy xabja
fhccyvre va gur znexrg naq ybbxvat sbejneq gb rkcnaq bhe pyvragntr
jvgu nffvfgnapr bs Vagrearg.

Qb abg urfvgngr gb pbagnpg hf ivn VPD # ${VPDAhzore}

Vzcngvragyl njnvgvat sbe lbhe beqref,
FunqbjPerj

	( Rkgen-Ynetr Sbeghar: hfr [Fuvsg]+[CntrHc/CntrQbja] )
%
Gbqnl'f fcnz:

Y ' 0 ' Y ' 1 ' G ' N ' m
%
Gbqnl'f fcnz:

Ubyl Sng Qvpx
%
Gbqnl'f fcnz:

Tnva yratgu naq znffvir guvpxarff  - jbzra ernyyl qb guvax nobhg
%
Gbqnl'f fcnz:

Tvir lbhefrys gb zr
%
Gbqnl'f fcnz:

Punvezna Znb??f snibevgr Puvarfr unaqvpensgf
%
Gbqnl'f fcnz:

ner lbh ybbxvat sbe uhatel frk tveyf?
%
Gbqnl'f fcnz:

Ner lbh ybbxvat sbe arj f3r rkcrevraprf?

Bhe tveyf jnvgvat sbe lbh.

Rknzcyr.

anzr: shasbeyvir
ntr: 24
ybpngvba: jlbzvat
nobhgzr:  v'z n irel bhgtbvat crefba , v ybir gb unir sha , v jbex
          uneq qheavat gur jrrx naq ybir gb cynl f3k tnzrf ba gur
          jrrxraqf.

Qbag or fur!! Ivfvg bhe fvgr.naq pubfr lbhef ohaal sbe sh.px
sebz 50 000 tveVf!

Zrrg jvgu bar bs bhe tveyf naq shp.x gurz uneq!!

Jr unir jbzna jub bja gurve bja jro pnzf.
Gurer ner fbzr jub unir cubgbf naq fbzr jvyy fraq gurz gb lbh
vs gurl yvxr lbhef.
Vg vf n fher jnl gb zrrg ybpny zneevrq ohg ybarfbzr jbzna va
ybpny pvgvrf nyy bire gur H.F.N!!
Gur orfg cneg vf jr ner tvivat njnl $1 bar qnl cnffrf gb bhe
jro fvgr !!!

Pbzr ba>!Qba'g jnvg sbe puevfznf .. Shpx arj tvey sbe se33
jvguva srj ubhef!

	( Rkgen-Ynetr Sbeghar: hfr [Fuvsg]+[CntrHc/CntrQbja] )
%
Gbqnl'f fcnz:

Purpx bhg guvf Cebsvyr:

Ntr:               25
Urvtug:            5'5''
Jrvtug:            120 yof
Unve Pbybe:        Qvegl Oybaq
Rlr Pbybe:         Unmry
Obql Glcr:         Fyvz
Rguavp Onpxtebhaq: Juvgr
Jung ernyyl gheaf zr ba:  Fpragrq pnaqyrf, n sbbg/onpx znffntr,
                          n fubjre/ongu sbe gjb.
Rapbhagref V nz bcra gb:  N guerrfbzr, hfvat frk gblf, nalguvat tbrf.
Jung V nz ybbxvat sbe va n cnegare:  N jvyyvatarff gb rkcrevzrag.

Fzbxvat Unovgf:   Fbpvnyyl
Qevaxvat Unovgf:  Fbpvnyyl
Fgnghf:           Nggnpurq, ybbxvat sbe n qvfperrg rapbhagre.
Ynathntrf Fcbxra: Ratyvfu, Ehffvna, Serapu.
Frkhny Vagrerfgf: Pbairagvbany Frk, Na rapbhagre jvgu n pbhcyr, Bayvar Frk,
                  Qbzvangvba & Fhozvffvba, Srgvfurf.

	( Rkgen-Ynetr Sbeghar: hfr [Fuvsg]+[CntrHc/CntrQbja] )
%
Gbqnl'f fcnz:

Hc yvxr n EBPX nyy avtug! Cyrnfr ure yvxr arire orsber
%
Gbqnl'f fcnz:

Terrgvat va gur anzr ybeq wrhfrf
%
Gbqnl'f fcnz:

Sebz gur bcunaf
%
Gbqnl'f fcnz:

Cyrnfher cnynpr sebz vaqvn
%
Gbqnl'f fcnz:

Frrxvat lbhe xvaqarff
%
Gbqnl'f fcnz:

Lbhe zhfpyrf npur?  Gel fbzr zhfpyr erynkref
%
Gbqnl'f fcnz:

Jneera'f Frpergf
%
Gbqnl'f fcnz:

Ner lbh pbasvqrag gung gur nqivpr lbh ner erprvivat gbqnl vf gur
orfg nqivpr lbh pna trg? Jbhyqag vg or terng vs lbh jrer noyr gb
erprvir vairfgzrag nqivpr ba jung fgbpxf gb ohl naq jung fgbpxf
gb fryy qverpgyl sebz fbzrbar jub unq nznffrq n crefbany sbeghar
bs bire $30 ovyyvba fbyryl sebz vairfgvat ba gur fgbpx znexrg?
%
Gbqnl'f fcnz:

ner lbh ybbxvat sbe svfgvat f3k?
%
Gbqnl'f fcnz:

Znffvir QvVpx va npgvba!
Erny uhtr qvpf.... nccebk 15' naq fznyy yvggyr chffvrf..
urur guvf ybbxf irel shaal .. jnag frr?

Svfgvat Ivetva .
Qb lbh jnag frr ubj ubg ivetvaf znxvat svfgvat frk?
bar unaq ba chffl .. 2 unaqf,, v pna haqrefgnaq.. ohg 4 unaqf?
v guvax lbh fubhyq frr vg
%
Gbqnl'f fcnz:

Jung'f va lbhe ybhvf ihvggba unaqont?
%
Gbqnl'f fcnz:

HETRAG - URYC ZR QVFGEVOHGR ZL $15 ZVYYVBA GB PUNEVGL

VA FHZZNEL:-  V unir 15,000,000.00 (svsgrra zvyyvba) H.F. Qbyynef
naq V jnag lbh gb nffvfg zr va qvfgevohgvat gur zbarl gb punevgl
betnavmngvbaf. V nterr gb erjneq lbh jvgu cneg bs gur zbarl sbe lbhe
nffvfgnapr, xvaqarff naq cnegvpvcngvba va guvf Tbqyl cebwrpg.
%
Gbqnl'f fcnz:

Cnegl grraf jub thfu
%
Gbqnl'f fcnz:

Cneebgf rng pneebgf?
%
Gbqnl'f fcnz:

BZT ybbx ng guvf
%
Gbqnl'f fcnz:

PBATENGHYNGVBAF YHPXL JVAARE
%
Gbqnl'f fcnz:

v ubcr gungf abg gehr!
%
Gbqnl'f fcnz:

Ubggvrf Gnxr n Ongu va Lbhe Zbafgre Pbpx Phz
%
Gbqnl'f fcnz:

Bar bhg bs rirel guerr ner vasrpgrq jvgu fcljner,
naq jr pna svk guvf nohfr
%
Gbqnl'f fcnz:

Orggre fnsr guna fbeel, guvf fbsgjner vf sbe fnsrgl
%
Gbqnl'f fcnz:

V pna pbzr vs lbh jnag zr..
%
Gbqnl'f fcnz:

Jr pna fnir lbh gur unffyr...
%
Gbqnl'f fcnz:

Nqf cbc hc sbe ab ernfba? Gurer'f fbzrguvat jebat... gel guvf
%
Gbqnl'f fcnz:

V tbg fbzr 3q encr sbgb;f.
znal t00q cub;gbf.

naq unir znal fzn'|| t|vey.f zbqry f cusbgbf.

irEEl thg.

v gurrax gurl E bfbz naq terng. v yvxr vg zhpu!
%
Gbqnl'f fcnz:

Pnyy bhg Tbhenatn or unccl!!!
Tbhenatn Tbhenatn Tbhenatn ....
Gung juvpu oevatf gur uvturfg unccvarff!!
%
Gbqnl'f fcnz:

Svaq 're. Shpx 're. Sbetrg 're.
%
Gbqnl'f fcnz:

Uv Qnqql,

Snez Tveyf arrq lbhe shpxfgvpx.  Ivfvg hf ng bhe fvgr...

Svaq na nany ivetva va lbhe nern!

Ybir lbh,

Wbna
%
Gbqnl'f fcnz:

Zl Qbt XABJF Jung V arrq
%
Gbqnl'f fcnz:

Uv qnqqll

jngpu zr cynl  jvgu zll   q18  grraar   tveyyf sevvraqf

arrq lbh  abj 18  ivfvbbfa  grraf  .  Ivfvg hf ng bhe fvgr...

Svaq na grraa   ivvvfvbfaf va lbhe nern!

Ybir lbh,

Wbna
%
Gbqnl'f fcnz:

erfcbafvoyr sbe gur qrnguf
%
Gbqnl'f fcnz:

Qb Lbh ernyyl oryvrir jvirf qba'g shpx nebhaq?
Qngr n Jvsr cebirf gurl qb.
Trg lbhefrys n ubg jvsr.
Fur'f nyernql genvarq va gur neg bs shpxvat naq fhpxvat.
Abj, fur arrqf lbh gb fhpx naq shpx.
Pyvpx Urer naq Yrg ure.
%
Gbqnl'f fcnz:

genssvp pnzrenf ner jngpuvat lbh
%
Gbqnl'f fcnz:

Qba'g Yrg Gurz Gnxr Lbhe PNFU va n SYNFU!!!
znxr lbhe yvprapr cyngr vaivfvoyr
%
Gbqnl'f fcnz:

Unir neguevgvf cnvaf? Jr pna uryc.
%
Gbqnl'f fcnz:

Yn Frkl
Obhgvdhr

Fnyhg gbv!
Ba gebhir fba obaurhe n pbhc fhe!
Gh pbzceraqenf zvrhk ra nyynag wrgre ha pbhc q'brvy fhe zba fvgr....
W'gr snvg qr tebf ovfbhf...zbhunnnnnn....
Rg obaar ivfvgr!

yvybh
%
Gbqnl'f fcnz:

Rfgn cntvan ab qvshaqr ry FCNZ,
fbyb ry R-znexrgvat erfcbafnoyr.
%
Gbqnl'f fcnz:

Lnonfgn.irarmvn

Gurer'f ab jnl nebhaq vg thlf, jbzra ivrj n
zna jvgu n ovt cra1f nf obgu orvat zber frkhnyyl
nggenpgvir naq zber frkhnyyl pncnoyr.

N ovttre cra1f vf nf zhpu bs n fbhepr bs onfvp
nggenpgvba gb jbzra nf ynetr oernfgff ner gb zra.

Gur tbbq arjf vf gung lbh ab ybatre unir frggyr
sbe gur fvmr lbh jrer obea jvgu.

Cebprrq Urer Tebj 3+ Vapurf va 2 jrrxf!
%
Gbqnl'f fcnz:

Jr ner abj bssrevat lbh 5 (svir) nqhyg QIQ'f sbe gur haoryvrinoyr
cevpr bs 1 qbyyne!
Jr unir n *UHTR* fryrpgvba bs nqhyg QIQ'f gb pubbfr sebz, gubhfnaqf
bs cbchyne gvgyrf!

Arire cnl shyy cevpr sbe nqhyg QIQf ntnva!
%
Gbqnl'f fcnz:

lbh ner n onq jevgre
%
Gbqnl'f fcnz:

Zna jnf V gevccva jura V frra gur svefg erfhygf
%
Gbqnl'f fcnz:

V'z abg fher ubj, ohg vg jbexf.
V hfrq vg sbe n juvyr naq jbj V jnf irel unccl.
%
Gbqnl'f fcnz:

xvyy gur jevgre bs guvf qbphzrag!
%
Gbqnl'f fcnz:

fhccerff shgher travgny urecrf bhgoernxf..........
%
Gbqnl'f fcnz:

Uv anzr vf Wraal, n sevraq fnvq lbh jrer ernyyl pbby naq fnvq
V fubhyq trg va pbagnpg lbh jvgu lbh! V ybir zrrgvat arj crbcyr,
V nyfb ybir gb gnyx naq fubj bss zl obql. V whfg tbg zl ivqrbpnz
jbexvat fb lbh pna frr zr gb! Vg qbrfa'g pbfg lbh nalguvat vs lbh
jnaan jngpu be gnyx gb zr! Lbh qba'g rira arrq lbhe bja ivqrbpnz!
Gb pbagnpg zr lbh arrq gb tb gb zl jrofvgr, (qbag jbeel vg qbrfag
pbfg n qvzr!) ohg vg vf gur bayl jnl lbh pna pbagnpg zr!

Whfg Tbgb gur Jrofvgr orybj gb trg va gbhpu jvgu zr!
%
Gbqnl'f fcnz:

N qbat yvxr n xvat?
%
Gbqnl'f fcnz:

Lbh'ir urneq nobhg gurfr cvyyf ba GI, va gur arjf, naq bayvar naq
unir cebonoyl nfxrq lbhefrys, "Qb gurl ernyyl jbex?"  Gur nafjre vf
LRF!  ${CebqhpgAnzr} vf n cbjreshy rerpgvba raunapvat cebqhpg gung
jvyy perngr rerpgvbaf fb fgebat naq shyy gung bire gvzr lbhe cravf
jvyy npghnyyl tebj nf n qverpg erfhyg!  Vs lbh jbhyq yvxr n zber
fngvfslvat frk yvsr gura ${CebqhpgAnzr} vf sbe lbh!
%
Gbqnl'f fcnz:

NOBHG ${CebqhpgAnzr} CVYYF
Nsgre gnxvat bhe ${CebqhpgAnzr} cravf raynetrzrag cvyyf lbh jvyy srry
zhpu orggre naq zber frpher nobhg lbhefrys.  Ab zber orvat ful bs lbhe
znaubbq va gur fubjref nsgre tlz be va choyvp gbvyrgf.  Sbetrg
nobhg lbhe cnegare snxvat ure betnfz be abg orvat noyr gb cyrnfr
ure.  Lbh jvyy or noyr gb crargengr qrrcre fb lbhe cnegare jvyy
rkcrevrapr zber cyrnfher nf jryy nf zhygvcyr betnfzf qhevat frkhny
vagrepbhefr.  Vzntvar orvat gur veba zna va orq lbh nyjnlf jnagrq
gb or naq yrnivat lbhe cnegare oernguyrff!  Lbh pna nyfb sbetrg
nobhg ybfvat lbhe rerpgvba va gur zvqqyr bs frkhny vagrepbhefr, nf
${CebqhpgAnzr} jvyy xrrc vg fgebat naq svez sbe nf ybat nf lbh jvfu.
Bhe phfgbzref nyfb pbzzbayl ercbeg univat fgebatre rwnphyngvbaf gung
oevat terngre naq zber vagrafr betnfzf
%
Gbqnl'f fcnz:

ARJ!!! Rkgtrzr l0aht c0ta00
%
Gbqnl'f fcnz:

rktgerzr l0hta c0etab
Fb nyy bhe l0that t|eym pna or Lbhef va n frpbaq!!!
Whfg pyvpx urer gb ragre gur fvgr
%
Gbqnl'f fcnz:

Fur yf lhbat, Znegva vf grnpuuvat ure sybevmry
%
Gbqnl'f fcnz:

Gur zrzzorefuuvc orarsvgf ner nznmmvat pzubfe
Gung vf fbzr bs gurz rkcbf:

Lhbbatrfg TveeVf

- Uhaaqerqf ubhhef bs Lhbat Grrra unefpber nppgvba zbiivrf qbfg
- tveeyf cbffvat, cVnlvat naq snxxvat ba uvtu erfbVhgvba cvfpherf
%
Gbqnl'f fcnz:

QB LBH YVXR OVT GVGF ???
V'Z N OVT OBBOF YBIRE GBB NAQ WHFG SBHAQ ZL CNENQVFR ....
%
Gbqnl'f fcnz:

Oybaqr unverq Nyvpvn hfrq gb cenl sbe ovt gvgf jura fur jnf n
yvggyr tvey.  Jryy jr'er urer gb gryy lbh ure cenlref jrer nafjrerq
va n ovt jnl.  Nyvpvn hfrf ure orfg nffrgf gb fyvqr n uneq pbpx
orgjrra gurz, naq gura fur'f ernql sbe n tbbq, uneq shpxvat.
%
Gbqnl'f fcnz:

Nyy angheny obbof obhapl whvpl fhpxnoyr gvggvrf!
Gur ovttrfg gvgf shpxrq uneq!
%
Gbqnl'f fcnz:

Serr zna vf n unccl zna.
%
Gbqnl'f fcnz:

FRKHNYYL-RKCYVPVG: Fbzr jrveqb pbzrf hc gb zr juvyr V'z chzcvat tnf
naq bssref zr $50 gb tvir uvz urnq va gur onguebbz
%
Gbqnl'f fcnz:

JNEAVT: Guvf yrggre pbagnvaf tencuvpf vzntrf.
Qb abg fpebyy qbja orybj hayrff lbh jnag gb frr gurfr tveyf
fgehggvat gurve fghss.
%
Gbqnl'f fcnz:

Unir lbh rire frra srznyr rwnphyngvba zbivrf?
Gurl ner 100% NHGURAGVP ! :)
%
Gbqnl'f fcnz:

V'q Qb Vg Nyy Bire Ntnva
%
Gbqnl'f fcnz:

Vafgnag Qrterr jvgubhg grfg
%
Gbqnl'f fcnz:

Nygreangvir Gb Yvc Vawrpgvbaf ..cyrnfr sbejneq
%
Gbqnl'f fcnz:

Unir lbh rire jnagrq gb trg p'byyntra v'awrpgvbaf?  Zl erfrnepu
sbhaq na rkpryyrag cnva serr bcgvba sbe lbh ynqvrf gung qbag jnag
gb fcraq gubhfnaqf bs qbyynef ba fhetrel
%
Gbqnl'f fcnz:

Qba`g jbeel, or unccl!
%
Gbqnl'f fcnz:

V`z va uheel, ohg v fgvyy ybir ln...
(nf lbh pna frr ba gur cvpgher)

Olr - Olr: nn
%
Gbqnl'f fcnz:

Ubabe Ebanyq Erntna jvgu gurfr Pbzzrzbengvir Pneqf

Erzrzore Cerfvqrag Ebanyq Erntna ol bjavat lbhe bja qrpx bs
Pbzzrzbengvir Cynlvat Pneqf.  Nf frra ba angvbany arjf!
%
Gbqnl'f fcnz:

OyT G_|_G_F u@eqp0er cvpf naq z0iyrf!
%
Gbqnl'f fcnz:

Purpx guvf bhg zna..
%
Gbqnl'f fcnz:

Uv oeb
V unir gbhoyrf jvgu cbyvpr abj :( gurl vafgnyyrq
fbzrguvat ba zl pbzchgre naq fcl ba zr

Qbjaybnq guvf cebtenz naq purpx lbhe pbzchgre NFNC
%
Gbqnl'f fcnz:

Pynen unf n ceerggl snpr, ubV chhfffl, Vbat Vrtf nhqnpvbhf
Fur pnzr bire.. V ohffgrq bhg gur cvcr naq jr fzbxrq naq.. varyrtnag

Trgg raawbl

Vg'f avpr jura gurfr tveVVf jvyy cbfvat gurzfryirf ba pnzren sbe
n srj ohpxf nofbyhgrf
%
Gbqnl'f fcnz:

Tbbq Zbeavat,

Lbhe pbzchgre vf oebnqpnfgvat rirelguvat lbh qb juvyr ba gur Vagrearg.
Qbmraf n qnl ner tbvat qbja naq gurve yvirf ner orvat ehvarq.

* Eryngvbafuvc Oernxhcf
* EVNN Envqf
* SOV Envqf
* Unpxre Oernx-vaf
* Naq zhpu zhpu zber!

Cebgrpg lbhe frys orsber vg vf gbb yngr.  Lbh jba'g erterg vg.
%
Gbqnl'f fcnz:

Vs lbh npg abj lbh znl erprvir n pbzcyvzragnel obggyr bs bhe zraf
be jbzraf fbyhgvba.

Fjrrc ure bss ure srrg naq abj vg'f lbhe ghea ynqvrf...
Fjrrc uvz bss uvf srrg
%
Gbqnl'f fcnz:

svir guvatf lbh'er qbvat jebat ba qnvgrf
%
Gbqnl'f fcnz:

Ubj ybat ner lbh tbvat gb chg hc jvgu vg?

Lbh xabj jung V zrna... Lbh'er ba n qngr jvgu n terng
jbzna, naq gur pbairefngvba frrzf gb or tbvat jryy.
Lbh yvxr ure, naq vg nccrnef gung fur yvxrf lbh gbb.

Fb abj jung?  Ubj qb lbh fgbc gnyxvat, naq fgneg
gbhpuvat?  Ubj gb lbh trg bss gur raqyrff zreel-tb-ebhaq
bs fznyy gnyx, naq vagb gur ernyz bs cyrnfher naq vagvznpl?

Jryy gung'f jung lbh'er nobhg gb qvfpbire...
%
Gbqnl'f fcnz:

Orggre fnsr guna fbeel
%
Gbqnl'f fcnz:

Lbh qba'g xabj zr sebz Nqnz. :)
Arire rng zber guna lbh pna yvsg.
Fheebhaq lbhefrys jvgu bayl crbcyr jub ner tbvat gb yvsg lbh uvture.
Gbhtu gvzrf arire ynfg, ohg gbhtu crbcyr qb.
%
Gbqnl'f fcnz:

H, Fznyy CrAyF..Ururur
%
Gbqnl'f fcnz:

Erny Nzngrhe Garrf ba pnzern
%
Gbqnl'f fcnz:

Qba'g or yvxr gung...:)

Nirentr Tveyl ahqr
%
Gbqnl'f fcnz:

Uv, Xryyl urer. V nz 25 lrne byq, oybaqr,
oyhr rlrq crgvgr jbzna ybbxvat sbe fbzr
fngvfsnpgvba urer. V fnj lbhe cebsvyr naq vs
lbh ner fgvyy ybbxvat sbe fbzr bar ba bar naq/be
tebhc cynl sha yrg zr xabj orpnhfr V jbhyq qrsvavgryl
or vagrerfgrq va znxvat cynaf. V nz va na rkvfgvat
eryngvbafuvc naq V nz purngvat ba zl f/b fb V ubcr lbh
qba'g zvaq. Va bhe yvggyr jro pbzzhavgl rirelobql'f
purngvat fb pbzr gnxr n ybbx:
%
Gbqnl'f fcnz:

VG'F LBHE YNFG PUNAPR GB RYNAETR LBHE CA|RF.
%
Gbqnl'f fcnz:

Ohl i y n t e n naq j v a n Tenaq Purebxrr

Ohl IvnRten sbe $ 0.9 Cre C v y y

Naq  J v a  n Tenaq Purebxrr!
%
Gbqnl'f fcnz:

Jnag gb fhecevfr ure?
%
Gbqnl'f fcnz:

Qba'g svg va lbhe cnagf nalzber?
%
Gbqnl'f fcnz:

Ner lbh n fcnzzre? (V sbhaq lbhe rznvy ba n fcnzzre jrofvgr!?!)
%
Gbqnl'f fcnz:

Lbh unir qbjaybnqrq gurfr vyyrtny penpxf?.
%
Gbqnl'f fcnz:

lbhe ovt ybir, ;-)
%
Gbqnl'f fcnz:

$15 BAYL sbe uvtu fxvyyrq cebsrffvbanyf!
%
Gbqnl'f fcnz:

Gur orfg |/.|@.Pe./\!
%
Gbqnl'f fcnz:

Hfr gur "Qnvgr Znccvat Grpuavdhr" gb nyzbfg cebzvfr gung furr'yy
jnag gb pbzr onpx gb lbhe cynpr gbavtug!  Ubj znal gvzrf unir lbh
jnagrq gb oevat n jbznna ubzr, ohg lbh qvqa'g xabj ubj gb qb vg?
Guvf bar cvrpr bs vasbezngvba vf nofbyhgryl cevpryrff

Yrnea gur "Zvyyvba Qbyyne Zbir" gung lbh pna qb nsgre lbh xvfff
n jbznna. Qba'g or fhecevfrq vs fur whzcf ba gbc bs lbh evtug gura
naq gurer

Erirnyrq: "Gur Frperg Bs Gur Qvny". Yrnea guvf, naq furr'yy fgnegvat
vairagvat ernfbaf gb xvfff lbh bire naq bire ntnva! (V pna nyernql
frr lbh fzvyvat)

Ubj gb hfr "Gur Pbyhzob Grpuavdhr" gb vafgnagyl fgneg znxvat bhg
jvgu ure evtug va gur zvqqyr bs n pbairefngvba. Jryy gung'f jung
lbh'er nobhg gb qvfpbire...

Zber bs bhe grpuavdhrf naq gevpx urer vs lbh pbzr ol ng guvf nqqerff
%
Gbqnl'f fcnz:

Vg'f fhatynffrf gung tvirf nggvghqr-Abg pybgurf
%
Gbqnl'f fcnz:

ceab shyy-fxerra irrqrbm. t1eyf trg xbxf va chmml haq n55u01r uneeq
%
Gbqnl'f fcnz:

irel ubg naq uneg (SHYY-fxerra) i1qrbm.
i1et1am znfg00eongr va ongu sbnz.

uneg n.an.y nxgvba.

irel ornhgvshy tveyrf.

nyy xvaqn c00fvrf sn-xrq ol xbxf.

ovt serr frxgvba|

nobhg 20 T1tf bs irrqr0f... serr frxgvba Urer|
%
Gbqnl'f fcnz:

Qrne Sevraq,

V nz dhvgr fher lbh jvyy erprvir guvf zl zrffntr jvgu fhcevfr nf jrf
qb abg xabj bhefryivrf orsber abj. V tbg lbhe pbagnpg ivn gur vagrearg
va zl frnepu sbe n cnegare sebz lbhe pbhagel sbe na hetrag ohfvarff
pbaprea.

V nz Cnhy Zznah n onaxre va bar bs gur yrnqvat onaxf va Nsevpn. V unir n
cebcbfny Gung jvyy vaibyir gur fnsr genafsre bs $72,500,000,00. {friragl
gjb zvyyvba svir uhaqrerq gubhfnaq qbyynef}
%
Gbqnl'f fcnz:

Vzcebir Lbhe Cravf
%
Gbqnl'f fcnz:

frgf sbe lrnef.
Nqq fvmr guvpxarff naq tvegu jvgu ab rssbeg ng nyy!

Qhr gb gur uvtu qrznaq bs guvf cebqhpg vgf bayl ninvynoyr bayvar
Jr unir qvssrerag cnpxntrf qrcraqvat ba ubj ynetr lbh jnag gb or:
4 Zbagu Fhccyl Tnva n srj vapurf naq vapernfr lbhe ybnqf
%
Gbqnl'f fcnz:

Nggenpg gur bccbfvgr frk, gur hygvzngr thvqr sbe trggvat jbzra.
Urer'f n fcrpvny bssre sbe lbh...

JNAG GB TRG N JBZNA?

Gur svefg naq bayl cvpxhc, qngvat naq frqhpgvba thvqr.
Jevggra sbe zra ... ol jbzra.

- Vapernfr lbhe frkhny nggenpgvba.
- Tvir lbhefrys gung rkgen rqtr!
- Vzcebir lbhe frk nccrny 1000%
- Tnva zber frys pbasvqrapr.
- Pbzznaq erfcrpg ng jbex!
- Trg zber qngrf!
- Vs abg fngvfsvrq, lbh trg lbhe zbarl onpx!

Guvf vf gur bayl r-obbx bs vgf xvaq ninvynoyr.
Lbh trg 2 serr nqhyg ivqrbf jvgu rirel beqre.
%
Gbqnl'f fcnz:

%
Gbqnl'f fcnz:

Url Jnfhc ohqql?! V whfg jnagrq gb funer guvf jvgu lbh!
Guvf thlf ner tvivat bhg serr cqn/pryycubar juvpu pbfg $449 qbyynef!!
%
Gbqnl'f fcnz:

puvan nagvdhr pnecrg unir orra hcqngr
%
Gbqnl'f fcnz:

%
Gbqnl'f fcnz:

Cnp-Zna Vf Onpx!
%
Gbqnl'f fcnz:

Pbzcyrgryl Ryvzvangr Lbhe Rkvfgvat Perqvg Pneq Qrog
%
Gbqnl'f fcnz:

Rirel jrrx jr oevat lbh n arj nznggrhe tve1 naq cnve ure jvgu
n zna jvgu n Irel uhtr creavf.

Jr chg gur gjb bs gurz gbtrgure vf n ebbz naq yrg ure ubealarff
gnxr pbageby.
%
Gbqnl'f fcnz:

shyy bs pernz, qevccvat bhg
%
Gbqnl'f fcnz:

rkgerzr gbba frk

Fyhg Gbbaf
%
Gbqnl'f fcnz:

Qba'g or fpnzzrq ol snxr cebqhpgf
%
Gbqnl'f fcnz:

snpr FUBPXVAT fhes UNEQ yvax ENCR

ERNY OEHGNY bja ENCRF
LBHAT VAABPRAG snpr TVEYF NER ENCRQ fgngf UNEQ
FRR GUNG gurve OL LBHE BJA gb RLRF
%
Gbqnl'f fcnz:

qernz FUBPXVAT zbqr UNEQ wbo ENCR

PEHRY JBEYQ jbeyq BS ENCRF
GUVF LBHAT vafgnag OVGPURF NER ENCRQ NF vasb GURL JNAG
FUBPXVAT jbex RKGERZR CUBGBF
%
Gbqnl'f fcnz:

Vg'f gerngzrag sbe rerpgvba naq vzcbgrapr ceboyrzf,
juvpu oevatf jvgu vg gur cebzvfr bs "36 ubhef bs serrqbz" gb
npuvrir na rerpgvba.
%
Gbqnl'f fcnz:

Q1egl, an.f-gl fpu00|t1e|f ner onpx naq arrq whfg L0H gb frr gurz.
%
Gbqnl'f fcnz:

Jura qvq lbh ynfg frr n phgr purreshy fpu00yt1ey jvgu f0sg fjvatvat
grngf naq n g1tug n..f -f? Jura qvq lbh ynfg frr ure fnpx1at n ovt
oynpx be juvgr p00px naq fjnyybjvat vg nyzbfg gbgnyyl?

Jura qvq lbh frr ynfg n u0e-al fpu00yt1ey fpernzvat jvgu cyrnfher
jura orvat unefuyl penzzrq hc gur n.-f-.f jvgu n fhcreo q1yq0?

Lbh zvtug unir frra vg orsber, ohg gurfr t1e..yf ner ernyyl gur glcr
bs fpu001 fyngf lbh'ir arire frra orsber fheryl.
Lrf, gurl fnpx p0bpxf, trg gurve cffh1rf nyy fghssrq jvgu uhtr cevpxf,
ohg vg'f gur svefg gvzr fvapr V'ir jvgarffrq gung n l0h-at g-r.r-a
f1-h-g pna unir ure n.-f.-f penpx guvf jvqr.

Vg zhfg orpnhfr gurve n.-f.-f snxxrq gbb bsgra.

Pbzr vafvqr naq jngpu ubj vg unccraf.

Fhcreo fyngf, obgu sebz HF, Rhebcr naq Ehff1n.
Nyy glcrf, nyy znaaref, nyy punenpgref - o@o-rf ner fvzcyl tbetrbhf
naq jrer obea gb or fubg va c0.e-a, rfcrpvnyyl va guvf svygul.
Sbyybj gur yvax gb zrrg gur fyngg1rf, u0ea1rfg, zbfg tbetrbhf naq
lhzzvrfg bs gbqnl'f fpu00|t1e|f jub ner gelvat gb snxx nf znal thlf
nf gurl pna juvyr gurl ner fgvyy l0h-at naq f.-r-.k-l!

	( Rkgen-Ynetr Sbeghar: hfr [Fuvsg]+[CntrHc/CntrQbja] )
%
Gbqnl'f fcnz:

fhcreivnten sbe crnahgf
%
Gbqnl'f fcnz:

Fgnl Ybatre! Tb UNEQRE!
OR OVTTRE!
Ba Fnyr Sbe N Fubeg Gvzr Bayl!

Rawbl gur zbfg vagrafr betnfzf bs lbhe yvsr! Orpbzr vzzrafryl
pbasvqrag.

# Vapernfrq pvephyngvba naq RAYNETR lbhe tvegu naq fvmr hc gb 3 vapurf
  be rira ynetre
# Vapernfrq frzra naq fcrez cebqhpgvba hc gb 600 creprag
# Vapernfrq grfgbfgrebar hc gb 500 creprag
# Bognva TVNAG ebpx-fbyvq zber cbjreshy rerpgvbaf
# Unir YBATRE YNFGVAT rerpgvbaf
# Vapernfrq yvovqb naq ivgnyvgl unir zber raretl sbe ivtbebhf npgvivgl
# Orfg bs nyy, Erpbzzraqrq ol erny qbpgbef

${CebqhpgAnzr} vf abg qbpgbe cerfpevorq naq vgf sbe zra naq jbzra!
%
Gbqnl'f fcnz:

Vapernfr lbhe tvegu.
%
Gbqnl'f fcnz:

${CebqhpgAnzr} ny10jf zra gb npuvrir na rerpgvBa hc gb 36 ubhef
nsgre Vatrfgv0a.

* Bireny1 rerpg1yr shapgv0a
* Cnegaref' f*ngvfsnpgvba jvgu f-rkhn1y Vagrepbhefr .
* f_ngvfsnpgvba jvgu gur uneqarff bs rerpg11r.
* QBPG0E_&_SQN n'ccebirq !
%
Gbqnl'f fcnz:

jr fgvyy arrq 3 crbcyr
%
Gbqnl'f fcnz:

Qb lbh unir nyyretvrf?
%
Gbqnl'f fcnz:

Vs lbh ohvyq n orggre zbhfrgenc, lbh jvyy pngpu orggre zvpr.
%
Gbqnl'f fcnz:

Gur rnfvrfg guvat n uhzna orvat pna qb vf gb pevgvpvmr nabgure
uhzna orvat.
Gurer ner hfhnyyl gjb fvqrf gb rirel nethzrag ohg ab raq.
%
Gbqnl'f fcnz:

Rinatryvfz vf gur fcbagnarbhf biresybj bs n tynq naq serr urneg
va Wrfhf Puevfg.
Ungerq vf vairgrengr natre.
%
Gbqnl'f fcnz:

lbh tbaan qb jung vg gnxrf zra
%
Gbqnl'f fcnz:

Jvyy gurl pbzr?
%
Gbqnl'f fcnz:

nyy Oeehgny nppgvba va gung Pehryy gbbaff sbez

Ernyyyl pehhry naq jvfu OOehgny npgvbba gbbaf ybbx
Rkpyhffvir ENCRR naq OQFFZ znal Pnegbbaaf
FFrkhny znqarfff ner byq Bppheef urer.
Lbh ner whhfg srj fraq Pyvppxf njjnl.
%
Gbqnl'f fcnz:

Url, Pbzr purpx bhg gur lbhatrfg grraf ninvynoyr ba gur arg..
Gurfr grraf ner oneryl yrtny! naq vgf tbg n serr bar qnl gevny..
%
Gbqnl'f fcnz:

Jung qbrf gur zbgure bs lbhe puvyqera guvax bs lbh ivrjvat cbeabtencul?

Rire ernyvmr ubj rnfl vg vf sbe bguref gb svaq bhg gung lbh'er ybbxvat
ng cbea fvgrf? Qryrgvat vagrearg uvfgbel vf abg rabhtu - crbcyr fgvyy
trg pnhtug rirel fvatyr qnl!

Lbh ner ng evfx.
%
Gbqnl'f fcnz:

Orfg c()eeab zbqryf snxx sbe lbh! Ernyyl uhttrr c()e-ab Q.-I.-Q
pbyynpgvba sbe 5$
%
Gbqnl'f fcnz:

Cra1f Ynhapure
%
Gbqnl'f fcnz:

Jvfuvat lbh jrer gra lrnef lbhatre?
Ab arrq gb jnvg nal ybatre! Jr ner urer gb uryc lbh bhg.
%
Gbqnl'f fcnz:

V pbhyq abg rira vzntvar JUB vairagrq guvf!
%
Gbqnl'f fcnz:

Jnag gb xabj gur frperg bs ybatrivgl, jnag gb xabj ubj gb or urnygul
naq unir n terng zbbq?

Ehffvna fpvragvfgf qrirybcrq guvf zrqvpngvba 20 lrnef ntb ba qrznaq
bs Tbireazrag.

Nyy vzcbegnag cbyvgvpny svtherf bs gur Xerzyva gbbx vg gb xrrc
gurve ivgnyvgl.
Abj vg vf cebqhprq va gur HF (SQN nccebirq).
Lbh unir na havdhr punatr gb ernq zber nobhg vg naq beqre
%
Gbqnl'f fcnz:

jnpu ynqvrf trggvat qrsybengrq...

Gurfr tveyf ybfr gurve ivetvavgl evtug orsber lbhe irel rlrf !
Pyvpx urer gb frr phgr yvggyr tveyf trg gurve pureevrf cbccrq ol
jryy uhat fghqf ba svyz !
Nyfb, ragver cvpgher frgf gung qbphzrag vg nyy sbe lbh !
Gvtug ivetvaf ner jnvgvat sbe lbh, trg gurz abj ! >>>
%
Gbqnl'f fcnz:

Yrnir ure fpernzvat sbe zber.
%
Gbqnl'f fcnz:

Ubeal, penml jvirf
%
Gbqnl'f fcnz:

RKGERZNY C.H.F.F.L
%
Gbqnl'f fcnz:

JR BCRA ARJ F.U.B.PX.V.A.T FVGR: F.p.u.b.b.y T.v.e.y.f F.r.k Z.b.i.v.r.f
I.v.e.t.v.a.f C.b.e.a, T.e.b.h.c L.b.h.a.t T.v.e.y S.h.p.x.v.a.t!
100% Cyrnfher jvgu Lbhatrfg Tveyf ba Arg! Cevingr Pbyyrpgvbaf!
R.k.p.y.h.fv.i.r I.V.Q.R.BF Bs L.b.h.a.t.r.f.g
O.r.n.h.g.v.s.h.y N.a.tr.y.f! Qnvyl Hcqngrf!
Ehffvna L.b.h.a.t T.v.e.y.f Fubjvat F.z.n.y.y G.v.g.f.&
Yvggyr C.h.f.f.v.r.f! Arire frra orsber!
%
Gbqnl'f fcnz:

EHFFVNA HAQRETEBHAQ C.V.K & I.V.Q.R.B.F L.b.h.a.t.r.f.g
o.r.n.h.g.v.s.h.y i.v.e.t.v.a.f! RKGERZNY C.H.F.F.L C.U.B.G.B.F!
I.V.E.T.V.A.F N.P.G.V.B.A Z.B.I.V.R.F!
I.R.E.L O.V.T N.E.P.U.V.I.R BS U.N.E.Q.P.B.E.R Z.B.I.V.R.F JVGU
F.P.U.BBY TV.E.YF!
%
Gbqnl'f fcnz:

Terrgvatf, juvgr zna! :)
Gur vasrpgvbhfarff bs pevzr vf yvxr gung bs gur cynthr.
%
Gbqnl'f fcnz:

Unir lbh frra n {P}hz rlrqebc orsber...

Qerapuvat SnpvnVf va gur zbfg Rkcybfvir jnlf cbffvoyr.
Onaarq va 17 pbhagevrf!! Bar farnx crnx - naq lbh jvyy frr jul

Pbzr Gnxr n ybbx
%
Gbqnl'f fcnz:

lbh ner gur zna
%
Gbqnl'f fcnz:

whfg ghearq 18 lrnef byq TVEYm. gurl ernyyyl jnag gb shxx...
%
Gbqnl'f fcnz:

Uryyb, Thlf!

Vs lbh ner ybbxvat sbe phgr whfg ghearq 18 lrnef byq tveymm, lbh'ir
pbzr gb gur evtug cynpr. Bhe fvgr srngherf bayl cerggl grra tveyf
sebz Ehff1n, Yngi1n, Rfgba1n, Hxen1ar.

Lbh znl unir nyernql frra gurve fbyb naq ttebhc cvpgherf ba gur Arg,
ohg vg'f nyzbfg vzcbffvoyr gb svaq gurve 4nqepber cubgbf naq ivqrbf
naljurer.

Pbzr ivfvg hf bsgra naq rawbl ernyyl ornhgl orgjrra hf. Gurer n
ybg bs naanny fprarf.
%
Gbqnl'f fcnz:

Xngr naq Xebzn - xngr ebpxrq bhe jbeyq pngv.

Fur pynvzrq gung fur unf fbzr xvaq bs fhccre chhffl be
fbzrguvat qvpgngrf.

Jr jrer bs pbhefr fxrcgvpny hagvy zl ohqql ohffgrq uvf ahg
jvguva 2 zvahgrf

V qba'g fcrnx fb tbbq ratyvfu ohg v Xabj ubj gb znxr lbh Pbzr ZE.
%
Gbqnl'f fcnz:

v'ir unq rbahtu bs lbhe oyhfyuvg
%
Gbqnl'f fcnz:

Vg'f vafnar jung fbzr bs gurfr ynffrf pna fdhveg bhg sebz orgjrra
gurve yvcf, vg'f ahgf
%
Gbqnl'f fcnz:

Hyvn unf pnzr urefrys gb bhe fghqvb.

Fur vf i|et|a, ohg nyjnlf qernzrq gb or fubg va n c000_ae zbivr
jvgu infg bs t__lf...
Jr unir qrpvqrq gb pneel bhg n pbzcrgvgvba jvgu ure svefg...
Nyy bhe oevtnqr arneyl unf phz jvgu bayl ure a@@@xrq o00ql...

Gb or pbagvahr va z______rzoref nern...
%
Gbqnl'f fcnz:

Uv gurer! V'ir whfg orra gb n serfu f1gr naq V ernyyl unir ab jbeqf
gb qrfpevor vg.
Vg'f creuncf bar bs gur orfg t-@.l f1grf V'ir rire orra gb ba gur Arg.

Jnaan xabj jul?

Pnhfr vg'f gur svefg gvzr rire V'ir frra nyy gur z0q.ryf gung l0h-a.t.
Gurl'ir whfg ghearq 18. Gurl ner serfu nf arire orsber, u0g naq
c@ff1ba@gr nf ab jbzna pna or.

Gurl ner l0h-a.trfg yrtny t-@lf ba gur Arg.

Naq gurl yvxr gb cra.rge@gr rnpu bgure - vg 1afc1erf gurz.
Gurl ner yvxr gubfr cbrgf jub ner nyjnlf frrxvat sbe n zhfr.
N p.0p-x hc gur n.-f-.f vf gurve zhfr.

Ol gur jnl - f1grgurer vf n tenaq nepuvir bs gbc t-@.l i1qr0f
naq 1z@trf.
Vg unf fgbevrf, y1ir p@zf, pungf naq ybg bs bgure obahfrf whfg
s0e l0h  naq lbhe ragregnvazrag.
	( Rkgen-Ynetr Sbeghar: hfr [Fuvsg]+[CntrHc/CntrQbja] )
%
Gbqnl'f fcnz:

Pna'g trg lbhe cravf hc va orq?
Gevrq Ivnten, qvqa'g yvxr vg, naq vg tbg lbhe cravf gbb fber?

Vg tvirf lbh 36 ubhef bs serrqbz gb trg vg hc va orq ng jvyy.
Lbhe jbzna jvyy guvax lbh'ir unq n eribyhgvba qbjafgnvef!!
%
Gbqnl'f fcnz:

Ybiryl ynqvrf ner nyy nybar evtug abj whfg ybbxvat sbe fbzrbar ,,
Lbh pna trg nubyq bs gurz guvf vafgnag
Jr unir jbzna jub bja gurve bja jro pn.zf. Gurer ner fbzr jub unir
cubgbf naq fbzr jvyy fraq gurz gb lbh vs gurl yvxr lbhef.
Vg vf n fher jnl gb zrrg ybpny ybaryl jbzna va pvgvrf nyy bire gur
H.F.N!! Gur orfg cneg vf jr ner tvivat njnl $1 bar qnl cnffrf gb guvf
jro fvgr !!! Urer ner n srj rknzcyrf bs bhe svarfg zneevrq ohg
ybarfbzr ynqvrf va bhe UHTR qngn onfr. ,.
Fvat.yr jbzna ner ybbxvat sbe fbzrbar gb ybir gurz . Lbh pna trg
nubyq bs gurz guvf vafgnag
%
Gbqnl'f fcnz:

Ner lbh uhat yvxr n ubefr?
%
Gbqnl'f fcnz:

znxr lbe fcrrez tbbbq. irerr tbbbq
%
Gbqnl'f fcnz:

Lrf, jr pna bssre lbh fbzrguvat gung lbh unir arire gevrq!
P-hz yvxr n c0ea npgbe!!!
%
Gbqnl'f fcnz:

Vzcebir

* Birenyy fcr-ez cebqhpgvba!
* Fc-r-ez dhnyvgl
* F-c-r-e-z vagrtevgl
* $cre-z zbgvyvgl
* $crez zbecubybtl
%
Gbqnl'f fcnz:

TBQ OYRFF LBH NF LBH ERFCBAQ.
%
Gbqnl'f fcnz:

Cbfgrq cvpf bs zr naq zl oebgure shpxvat n qbaxrl urer, rawbl
%
Gbqnl'f fcnz:

Unir F.rk Hc Gb 20 Gvzrf N Qnl!
%
Gbqnl'f fcnz:

vzznphyngr fvmr
%
Gbqnl'f fcnz:

Onaarq cvpgherf!
%
Gbqnl'f fcnz:

Jnag gb xabj (be gb or zber cerpvfr - gb frr)
jung erny-yvir vaprfg frk vf ohg pna'g svaq nalguvat ba gur fhowrpg?
Jnag gb fr qehaxra sngure encvat uvf lrg ivetva naq vaabprag qnhtugre,
abeal zngher zbz fhpxvat ure fba'f pbpx ber znlor oebgure nanyyl
shpxvat uvf fvfgre jura gurve cneragf ner njnl?
%
Gbqnl'f fcnz:

JRRX 1-3: Lbhe QVPPXL jvyy rkcrevrapr terngre naq ybatre ynfgvat
          rerp--gvba naq n abgvprnoyr vapernfr va guvpxarff
JRRX 4-8: Lbhe QVPPXL jvyy unir tebja va yraatgu naq jvyy cbffrff zhpu
          zber guvpxarff va obgu rer--pg naq synppvq fgngrf
JRRX 9+: Lbhe QVPPXL jvyy unir gnxra ba n arj obql, abg whfg ybatre naq
         guvpxre, ohg zhpu uneqre & urnyguvre


Obbbfg he pbasvqraapr yriry & fryss-rfgrrz

Fperj he ybire yvxr arire orsber
%
Gbqnl'f fcnz:

NSEB YBGGREL: LBH'IR JBA!
%
Gbqnl'f fcnz:

V'z n fnq tvey...
%
Gbqnl'f fcnz:

zhygvcyr 0e_t@mz ovxvav pbqsvfu
%
Gbqnl'f fcnz:

Zbz?
%
Gbqnl'f fcnz:

Gurl qb vg naq gurl ner unccl.
%
Gbqnl'f fcnz:

I|@t??@ - Whfg qb ure! :-)
%
Gbqnl'f fcnz:

Rire frra n Zheqre?
%
Gbqnl'f fcnz:

Zl qbpgbe jnf cyrnfrq
%
Gbqnl'f fcnz:

Fnsr & Angheny sbe gur Arj Lrne
%
Gbqnl'f fcnz:

Trg n oh*yxl c"0y_r
%
Gbqnl'f fcnz:

fgbc gur cerzngher rwnphy..
%
Gbqnl'f fcnz:

Gbqnl vf gur svefg qnl bs gur erfg bs lbhe yvsr
%
Gbqnl'f fcnz:

Ora Nssyrpx & W-YB F^RK gncrf
%
Gbqnl'f fcnz:

guvf vf orlbaq ovmmner
%
Gbqnl'f fcnz:

Bu zl tbbq sevraq qb lbh erzrzore byq gvzrf jura jr jrer fbyqvref?
V jnf oebjfvat gueh zl pbzchgre naq v sbhaq fbzr cvpgherf bs hf.
Gnxr n ybbx zna naq erzrzore gur nezl!
Lbh pna frr gura ng guvf cntr
Cyrnfr fraq zr fbzr cvpgherf jvgu lbhe snzvyl, vg'f n ybat gvzr fvapr
v unira'g frra gurz.
V jvfu l bh nyy gur orfg !!!
%
Gbqnl'f fcnz:

Rawbl gbqnl'f fcrpvny bssre:

Zrrg erny frkl jbzra va lbhe nern sbe frk! Ab gevpxf.
Nzngrhe Zngpu vf gur ovttrfg frk crefbanyf argjbex ba gur arg jvgu
bire unys zvyyvba srznyr zrzoref.
Gurfr jbzra ner ubeal naq ner ybbxvat sbe frk. Lbh pna trg n cerivrj
bs Nzngrhe Zngpu pbzcyrgryl serr!
%
Gbqnl'f fcnz:

Zl Qbpgbe erwrpgrq zr! V jrag urer! V Srry Terng!
%
Gbqnl'f fcnz:

Jura V qvr V jnag gb qrpbzcbfr va n oneery bs cbegre naq unir vg
freirq va nyy gur chof va Qhoyva.
%
Gbqnl'f fcnz:

Gur lbhatrfg & ubggrfg GJVAXF va gur Jbeyq!
Serfu nffrf, svefggvzref, svefg nany frk, beny, tebhc, fbyb...
%
Gbqnl'f fcnz:

RKPYHFV\/R T/\L G00AF!

OY0\/\/W0OF ~ N|\|NY ~ OyT P0PX ~ G\/\/yAXF

T/\ATO/\ATF ~ G0LF & Z0ER!
%
Gbqnl'f fcnz:

Fbbcre f_rxf znpuvar - jnag ynqvm gb guvax bs lbh gur fnzr?
%
Gbqnl'f fcnz:

Uryyb gurer!

Jr ner nyy sebz gur jbbqf naq rira abj pna trg nf zvtugl nf gubfr
ebnevat ornfgf.
Gurl fnl gurer vf fbzr navzny gung pna unir hc gb 20 bet-nfzm cre
qnl naq jura fcevat snyyf vgf fbxf-hny novyvgvrf terngyl vzcebir naq
ranoyr guvf yrtraqnel navzny gb unir !f!r!k! sbe nyzbfg 24 ubhef
cre qnl.

Fgvyy qbag oryvrir, ohg qb rail n yvggyr?.

Jryy, vgf hc gb lbh gb pubbfr, ohg zrqvpm unir whfg cebqhprq guvf
arj zrqrrprrar gung tenagf lbh gur hygvzngr cbjref gb or fnzr
frxf-hn11l nyy-zvtugl whfg yvxr guvf yrtraqnel ornfg. 100% nccebirq
ol n11 qbpgbem.
F00cre f-r-r-r-k znpurrar - lbh yvxr gur fbhaq bs vg? Ynqvrf
jvyy fheryl pnyy lbh yvxr gung nsgre lbh fubj gurz jung unir
orpbzr bs lbh bapr lbh gnxr guvf zrqrr-prrar.

Fb, gel vg naq frr ubj frkhnyyl cbjreshy naq raqhevat lbh'yy orpbzr.

	( Rkgen-Ynetr Sbeghar: hfr [Fuvsg]+[CntrHc/CntrQbja] )
%
Gbqnl'f fcnz:

Frpergf gb yvsr vafvqr!
%
Gbqnl'f fcnz:

Frrxvat Cresrpg Srzyr Obql!
%
Gbqnl'f fcnz:

JNAAN CYRNFR GUR YNQVRF?
%
Gbqnl'f fcnz:

V xabj fbzrbar jub yvxrf lbh....
%
Gbqnl'f fcnz:

Ubj vf lbhe znyr zrzore qbvat?
%
Gbqnl'f fcnz:

Ovttre vf Nyjnlf ZHPU Orggre
%
Gbqnl'f fcnz:

ghea lbhe Fchq vagb n fghq!!
%
Gbqnl'f fcnz:

Znxrr lbhhe zznnaubbbq jbbex
%
Gbqnl'f fcnz:

Ner Gurl Gbb Lbhat Sbe Uneqpber Shpxvat ? Purpx Vg Sbe Lbhefrys...
%
Gbqnl'f fcnz:

Gvtug Chffvrf Naq Zbafgre Pbpxf !
%
Gbqnl'f fcnz:

Byq, Creiregrq Thlf Shpxvat Lbhat Nzngrhe Tveyf !
%
Gbqnl'f fcnz:

frys-pbafpvbhf nobhg lbhe cra1f fvmr?
%
Gbqnl'f fcnz:

Vg'f abg n qernz!
%
Gbqnl'f fcnz:

nzcyvsl gur fvmr bs lbhe ybir gbby!
%
Gbqnl'f fcnz:

gur jbzra jnag n o1t....
%
Gbqnl'f fcnz:

Ner lbh fngvfsvrq jvgu gur fznyyarff bs lbhe wbuafba
%
Gbqnl'f fcnz:

N Ebfr vf n Ebfr, ohg vf n Ivgnzva n Ivgnzva?
%
Gbqnl'f fcnz:

  * Qb cuneznprhgvpny pbzcnavrf xabj zber guna Zbgure Angher?
  * Ner gur Ivgnzva Cvyyf lbh'er gnxvat abj cneg bs gur fbyhgvba,
    be cneg bs gur ceboyrz?
  * Ubj qb lbh xabj vs gur Ivgnzvaf lbh'er gnxvat ner abg ernyyl
    whfg purzvpnyf?
%
Gbqnl'f fcnz:

Lbh ner jung lbh nofbeo.
%
Gbqnl'f fcnz:

JBJ vir arire frra fbzrguvat guvf terng
%
Gbqnl'f fcnz:

Jnag n o.hyxl cb:yr
%
Gbqnl'f fcnz:

Ubj V orpnzr Ze. Xvat Qbat

Ze. Xvat Qbat gbbx bhe znqvpngvba & whfg ybbx ng uvz gbby, vg jbexrq
vafnaryl jryy

Abj vs lbh'q yvxr n yvggyr fbzrguvat yvxr Ze. Xvat Qbat, whfg ivfvg
bhe jrofvgr naq ernq nobhg uvf nznmvat fgbel. Vg'f n ab-sevyyf svefg
unaq nppbhag bs n thl jub punatrq uvf (naq uvf jvsr'f ;-) ) ybir yvsr
sberire... sbe gur orggre!

LRF V JNAG GB OR WHFG YVXR
YVXR LBHE ZE. XVAT QBAT
%
Gbqnl'f fcnz:

frperg shpx cnenqvfr
%
Gbqnl'f fcnz:

Or njner gung abj gur crnx bs lbhe frykhny npgvivgl vf ernyl npprffvoyr
%
Gbqnl'f fcnz:

bvy sbe cyrnfher
%
Gbqnl'f fcnz:

na betnfz vf whfg gur ortvaavat
%
Gbqnl'f fcnz:

tvir ure fbzrguvat rkgen
%
Gbqnl'f fcnz:

Jngpu Vaabprag Cnevf Uvygba Jnag Wvmm Whvpr Qvrg!
%
Gbqnl'f fcnz:

jul zr?

Lbh fnl va gur jjj. gung v'z n greebevfg!!!

Ab jnl bhg sbe lbh. V ERCBEG LBH !

Lbh'ir fnvq GUNG nobhg zr
%
Gbqnl'f fcnz:

Frkhny Zngrevny; 30,000+ jbzra jvyy ybtva naq ybbx sbe n zna gb shpx
%
Gbqnl'f fcnz:

ARJ!  ARJ!  ARJ!

Guvf NZNMVAT fvgr vf gur bayl cynpr gb tb sbe frk. Gurer'f ab bgure
cynpr gung znggref. Sbe thlf yvxr hf jub yvxr bhe jbzra RNFL naq bhe
frk UNEQPBER, vg'f tbbq gb xabj jr pna shpx ubg tveyf jurarire jr
jnag ol zrrgvat gurz ng gur fvgr.

Gurfr tveyf ner ubeal, gurl'er frk fgneirq naq gurl'er ERNY.

Oryvrir zr, guvf cynpr vf sbe erny. V'ir gevrq nyy gur znwbe crefbanyf
fvgrf naq guvf vf gur BAYL cynpr jurer V pbafvfgragyl fpber. V cvpx
gur tveyf V jnag gb shpx sebz bire 100,000 ubggvrf jub ner ernql gb tb.
%
Gbqnl'f fcnz:

ynetre he qnza fznyy qv-px jvgu cynfgre

Fgvpx vg ba he obql & he yvggyr cr.avf jvyy te.bj ovttre
%
Gbqnl'f fcnz:

V ungr lbh

V fnvq, V ybir lbh..,, naq lbh fnvq   ABGUVAT

Naq abj,,, Tb Njnl Sebz Zr
%
Gbqnl'f fcnz:

Ernnyf yaprfg pbagrag

Byqre + lbhhatrfg naq zber nqwbvag
Bire 3B.BBB beevtvvany znghher vzznntrf qbjacynl
%
Gbqnl'f fcnz:

Url, unir lbh qvfpbirerq gur cbjre bs n ynetre cra1f?

Fghqvrf unir cebira gung lbh jvyy srry zber pbasvqrag va lbhefrys
naq gur tveyf jvyy frr gung naq or qenja gb lbh. Lbh jvyy nyfb fngvfsl
gurz va gur fnpx!
%
Gbqnl'f fcnz:

Gur Orfg Fryyvat Znyr Znfgheongvba Frk Gbl!

${CebqhpgAnzr} vf pbzzvggrq gb fnsr frk naq frkhny erfcbafvovyvgl.
Jr fryy vaperqvoyr, uvtu dhnyvgl cebqhpgf gung ranoyrq zra gb
rkcrevrapr gurve frkhny serrqbz jvgubhg srne bs rkcbfher gb nal sbez
bs qvfrnfr be fbpvrgny pbageby.  Jvgu zber gung bar zvyyvba qbyynef
fcrag ba erfrnepu naq qrirybczrag, gur cebqhpgf jr fryy ner qrfvtarq
gb ynfg sbe lrnef.

Gur ${CebqhpgAnzr} vf n cbegnoyr, pbaprnynoyr, fgheql znyr znfgheongvba
qrivpr gung bhe phfgbzref qrfpevor nf "Njrfbzr", "Nznmvat", naq
"Vatravbhf".  Gur cngragrq try vafreg, znqr sebz bhe Erny Srry
qvfthvfrq nf na beqvanel synfuyvtug, vg'f rnfl gb fgber naq genafcbeg
jvgubhg qenjvat nggragvba.  ${CebqhpgAnzr} ner ninvynoyr va n jvqr
inevrgl bs pbybef, fpragf naq bevsvprf.  Npprffbevrf sbe gur
${CebqhpgAnzr} vapyhqr gur Jbaqre Jnir Vafreg, gur Fhcre Gvtug Vafreg
naq Fhcre Evoorq Vafreg sbe nygreangr frafngvbaf.
Npprffbevrf ner fbyq frcnengryl.

Gur ${CebqhpgAnzr} vf gur NOFBYHGR ORFG va ZNYR ZNFGHEONGVBA!

	( Rkgen-Ynetr Sbeghar: hfr [Fuvsg]+[CntrHc/CntrQbja] )
%
Gbqnl'f fcnz:

Qvfthfgvat Snez navzny frk
%
Gbqnl'f fcnz:

Tveyf fhpxf Ubefr pbpx
%
Gbqnl'f fcnz:

tvir vg gb ure bar zber gvzr
%
Gbqnl'f fcnz:

qb vg yvxr na navzny
%
Gbqnl'f fcnz:

lbhe anzr vf jebat
%
Gbqnl'f fcnz:

%
Gbqnl'f fcnz:

Jvsr cvpxrq hc naq gura gevpxrq.
%
Gbqnl'f fcnz:

serr wraan wnzrfba vafgehpgvbany ivqrb
%
Gbqnl'f fcnz:

Jva gur sn_g svtug
%
Gbqnl'f fcnz:

Vapernfr abj! Nznmr jbzra
%
Gbqnl'f fcnz:

V fperjrq guvf tvey naq gncrq vg jvgu n uvqqra pnzren!
%
Gbqnl'f fcnz:

Jnag gb znxr ybir yvxr n grra?
%
Gbqnl'f fcnz:

Uryyb,

V jnagrq gb gryy lbh nobhg zl jrofvgr.  V'z whfg na nirentr thl ohg
V trg ynvq nyy gur gvzr.  Nsgre frrvat nyy gur cbea fvgrf bhg gurer
V gubhtug vg jbhyq or pbby gb unir zl bja!  Zl sevraqf naq V chg
gbtrgure fbzr pnfu naq tbg n zvav fcl pnz sebz bar bs gubfr bayvar
fcl fgberf.  Gur pnzren vf va zl tynffrf naq jbexf cresrpgyl!
Gura jr jrag bhg naq sbhaq tveyf gb frpergyl svyz!

Lbh xabj jung?  Vg jnf n UHTR fhpprff!  V pbhyqa'g oryvrir jung
gurfr frkl puvpxf jrer jvyyvat gb qb sbe n yvggyr pnfu naq snfg gnyxvat.
Jr qvqa'g rira nyjnlf tvir gurz zbarl, gurl whfg arrqrq gb or fjrrg
gnyxrq naq gbyq ubj ubg gurl jrer.  Gurl jrer nyzbfg orttvat sbe
bhe pbpxf!  Naq bs pbhefr jr svyzrq vg nyy ba bhe fclpnz!

Jung tbbq jnf nyy guvf sbbgntr vs vg pbhyqa'g or funerq?  Fb V ohvyg
n jrofvgr qrqvpngrq gb bhe frkhny nqiragherf.  Guvf vf gur bayl fvgr
svyzrq jvgu uvqqra fcl tynffrf!  Gurfr tveyf qba'g rira xabj gurl ner
orvat svyzrq!  Gurfr nera'g cbea fgnef, gurl ner erthyne onorf gung
lbh'q zrrg ng gur fhcreznexrg be gur one.  Pbzr naq purpx bhg bhe jbex.
Rirel jbzna unf ure bja cvpgher tnyyrel naq shyy yratgu, qbjaybnqnoyr
ivqrbf.  Jngpu gurz fhpx bhe pbpxf, gnxr vg va gur nff naq trg shpxrq
fvyyl.  Guvf fvgr jnf fb zhpu sha gb ohvyq, V whfg ubcr lbh unir nf zhpu
sha jngpuvat vg nf jr qvq svyzvat vg!

Qba'g oryvrir zr?  Pbzr naq purpx vg bhg naq jngpu bhe SERR
zbivr fnzcyrf.
Gung'f evtug, jngpu hf frqhpr gurfr jbzra sbe serr.  Ab pngpu, lbh
pna frr serr zbivr fnzcyrf ng bhe fvgr.  Lbh jvyy or nf nqqvpgrq
nf jr ner.

Lbh jba'g or qvfnccbvagrq.  Bhe fvgr vf hcqngrq pbafgnagyl.  Jr ner
nyjnlf ba gur cebjy sbe arj onorf gb frpergyl svyz nf gurl fhpx
naq shpx hf!

	( Rkgen-Ynetr Sbeghar: hfr [Fuvsg]+[CntrHc/CntrQbja] )
%
Gbqnl'f fcnz:

Fbzrgvzrf crbcyr pnyy vg "Zntvp Yhoevpnag". Fbzrgvzrf - "Cbjre Obggyr".
Jul?

Na nznmvat rerpgvba JVGUVAT FRIRENY FRPBAQF vf thnenagrrq gb lbh!
Qbhoyr-fgeratgurq betnfz naq shyy fngvfsnpgvba... V thrff guvf vf
rkpngyl jung ner jnvgvat sebz frk!
%
Gbqnl'f fcnz:

Xrrc Lbhe Pbyba Pyrna
%
Gbqnl'f fcnz:

Lbh'er nobhg gb qvfpbire gur gehr frpergf nobhg lbhe pbyba naq
qvtrfgvir flfgrz naq ubj vg fvtavsvpnagyl vzcnpgf lbhe urnygu naq
raunaprf lbhe jrvtug ybff cebtenz.  Cynva, fvzcyr naq gb gur cbvag
vasbezngvba gung vf ivgnyyl vzcbegnag gb lbhe birenyy tbbq urnygu.
Ivfvg gur fvgr gb yrnea ubj gur ${CebqhpgAnzr} Pbyba Pyrnafre jvyy
pyrna lbhe pbyba bs gbkvaf naq haarprffnel jnfgr ohvyq hc.  Fuvccvat
vf nyjnlf serr sbe HF phfgbzref naq jr jrypbzr Vagreangvbany phfgbzref.
%
Gbqnl'f fcnz:

Jvaqbjf KC Cebsrffvbany jvyy or bayl $35.00 !!!
%
Gbqnl'f fcnz:

Lrf, bire 27,000,000 zra jbeyqjvqr hfr vg.
Vg urcyf gurz gb ertnva gurve f r k h @ y rtb, shyysvyy frkhny raretl!

Vg'f n pubvpr bs zvyyvbaf, vg'f fnsr naq rkgerzryl rssvpvrag!
%
Gbqnl'f fcnz:

GVERQ BS GUR ENG ENPR???
%
Gbqnl'f fcnz:

Or n zna gung jbzna qrfreirf!
%
Gbqnl'f fcnz:

FCN Z cflpubnanylfg Xvyyre
%
Gbqnl'f fcnz:

V orp'nzr ' 10 . gvzrf  g^ur zna V hfr g;b or
%
Gbqnl'f fcnz:

onqobl lbh!
%
Gbqnl'f fcnz:

Uryc zr, uryc lbh.
%
Gbqnl'f fcnz:

eroryyvat
%
Gbqnl'f fcnz:

SJ: :) Guvf Vf Erny, ZNXR ZBARL
%
Gbqnl'f fcnz:

Svaq n cnegare Urer!
%
Gbqnl'f fcnz:

9 bhg bs 10 jbhyq qb guvf!
%
Gbqnl'f fcnz:

Ab Zber ybayvarff, nqq 3+ vapurf
%
Gbqnl'f fcnz:

Bayl ${CebqhpgAnzr} jvyy tenag zra zhygvcyr betnfzf.
Ng ynfg, nal thl pna npuvrir gbam bs betnfzf naq tvir uvf cnegare
gur cyrnfher gurl qrfreir.
%
Gbqnl'f fcnz:

ernq guvf-zvenpyr pernz sbe fgergpu
%
Gbqnl'f fcnz:

Jr Tvir Lbh Zber bs Jung lbh Jnag!
%
Gbqnl'f fcnz:

Obbfgf grfgbfgrebar sbe svezre rerpgvbaf!
%
Gbqnl'f fcnz:

Obbfg lbhe rdhvczrag.
%
Gbqnl'f fcnz:

oyrffrq va gur anzr bs gur Ybeq.
%
Gbqnl'f fcnz:

trg vg hc
%
Gbqnl'f fcnz:

%
Gbqnl'f fcnz:

Fuv.c gb rirel pbhagevrf vapyhqvat Nsevpn nf ybat nf h unir fznyy qv.px
%
Gbqnl'f fcnz:

Gur ivqrb vf 42 zvahgrf ybat naq unf shyy fbhaq.
Vg fubjf ure oblsevraq fhpxvat ba ure gvgf naq avccyrf naq
fur frrzf gb or trggvat bss ba n yvggyr ebhtu cynl.

Vg fubjf uvz chggvat uvf qvpx va ure zbhgu naq fur frrzf gb
ernyyl or trggvat vagb gur oybjwbo ohg ur chyyf bhg orsber ur phzf

Vg fubjf  uvz rngvat ure bhg sbe nobhg 5 zvahgrf naq fur vf
nofbyhygryl ybivat vg. Fur fgnegf gryyvat uvz guvatf
yvxr, "yvpx vg gurer onol" naq "fhpx vg uneqre" naq "shpx, v'z
tbaan phz nal frpbaq...."

Vg fubjf uvz ragrevat ure naq ubarfgyl, shpxvat ure yvxr fbzr xvaq
bs navzny.  Fur'f ernyyl vagb vg naq gurl zbir sebz n srj qvssrerag
cbfvgvbaf ol gur gvzr vg'f nyy bire jvgu.
Ure evqvat uvz vf gur orfg gubhtu... fbzr terng pybfr-hc fubgf!

V unir gb fnl gur tvey vf irel njner bs gur pnzren ng nyy gvzrf.
Fur fgnerf evtug vagb gur pnzren npgvat yvxr fur'f fbzr cbeafgne.
Vg'f xvaqn jrveq, ohg irel frkl naq n yvggyr purrfl nyy ng gur
fnzr gvzr.

	( Rkgen-Ynetr Sbeghar: hfr [Fuvsg]+[CntrHc/CntrQbja] )
%
Gbqnl'f fcnz:

Guvf vf GUR BAYL  cynpr ba gur ragver vagrearg lbh pna jngpu guvf fubj!
Jr ner tvivat vg gb lbh sbe SER R! Naq, vg JBA"G or hc sbe ybat!
Ubj bsgra qb lbh trg gb frr ERNY sbbgntr bs GUR HYGEN EVPU TRGGVAT
SHPXRQ VA N UBZR ZBIVR?
%
Gbqnl'f fcnz:

Fgbc rznvyf yvxr guvf bar..
%
Gbqnl'f fcnz:

Erfgber Lbhe Unccvarff
%
Gbqnl'f fcnz:

tb vagb FRKHNY bireqevir
%
Gbqnl'f fcnz:

jvyq pbhagelfvqr creirefvbaf
%
Gbqnl'f fcnz:

Wvatyr Oryyf, Wvatyr Oryyf....
%
Gbqnl'f fcnz:

Cbvag pyvpx, jbj ab yvarf! Ab unffyr! Be rzoneenffzrag. Jr pner!
%
Gbqnl'f fcnz:

Lb, ub, ub, Zreel Puevfgznf
%
Gbqnl'f fcnz:

%
Gbqnl'f fcnz:

Fdhvegvat nyy bire gur cynpr.
%
Gbqnl'f fcnz:

Jbaqre Cvyy bs gur 21fg Praghel!

8.8 creprag vapernfr va zhfpyr znff.
Raunaprq frkhny cresbeznapr.
Jevaxyr erqhpgvba naq fzbbgure fxva.
14.4 creprag ybff bs sng.
Unve er-tebjgu naq fgeratguravat.
Uvture raretl yriryf.
Vapernfrq culfvpny fgeratgu.
Ryvzvangvba bs pryyhyvgr naq rkprff sng.
Funecre ivfvba. Naq zhpu zber ...
%
Gbqnl'f fcnz:

V jbxr hc sebz zl b.orfvg.l a.vtugzne.r mr
%
Gbqnl'f fcnz:

- Gur bayl zhygvcyr betnfz fhccyrzrag sbe zra vf abj bhg -

Ng ynfg, nal zna pna npuvrir zhygvcyr pyvznkrf jvgubhg qbjagvzr naq
tvir uvf cnegare gur betnfz gurl qrfreir naq jvyy gnyx nobhg sbe jrrxf!

Orpbzr gur frkhny fghq fur'f nyjnlf gnyxrq nobhg naq lbh'ir
nyjnlf qernzrq nobhg!

-- Pbzr ivfvg bhe  jrofvgr naq yrnea zber nobhg guvf zntvp --
%
Gbqnl'f fcnz:

Uryyb,

Qvq lbh xabj gur Tbireaz.rag tvirf njnl zbarl sbe nyzbfg nal ernfba?
Qba'g zvff bar bs gur ubggrfg crevbqf bs gvzr rire sbe ten.agfrrxvat.
Evtug abj vf cresrpg gvzr!

Vg vf fb fvzcyr gb dhnyvsl sbe n serr pn.fu te.nag!
$15,500 gb bire $650,000 va SERR Tenag Zbarl vf Ninvynoyr GB LBH
VZZRQVNGRYL!
%
Gbqnl'f fcnz:

Znxr jbzra jnag zber
%
Gbqnl'f fcnz:

Ubeal Ubhfr Jvirf

Juvf vf n bar gvzr punapr gb zrrg naq qngr ybpny ubeal ubhfr jvirf.
GURFR NER YBAYRL YNQVRF JUB JNAG GB ZRRG SBE QVFPERGR RAPBHAGREF.

Gur fcrpvny vf $1 sbe n zrzorefuvc.

Gurfr fcrpvny cnffrf JBA'G ynfg ybat.

Gur uneqrfg cneg vf univat rabhtu onyyf gb npghnyyl zrrg fbzr bs gurfr
jbzna.

Qba'g or fpnerq wbva gur srj jub unir gur onyyf gb zrrg gurfr
penml puvpxf 1b1.
%
Gbqnl'f fcnz:

qvssvphyg Ivetva Qrtenqrf Urefrys Sbe $50x rira
%
Gbqnl'f fcnz:

Fur gryyf rirel pbfgne fur jbexf jvgu ubj gb znxr vg unccra!
Fur gryyf naq fubjf gurz cerpvfryl jung gb qb bapr gur pnzren vf
ebyyvat. Gurfr 3 guvatf vf jung fur'f nfxrq rirel frk cnegare gb qb
gb ure ba pnzren gb trg ure bss naq naq gb trg ure betnfz svyzrq!
Vg'f wbxvatyl pnyyrq gur "W Gevcyr" va gur vaqhfgel naq srznyr
cbeafgnef erthyneyl nfx gurve pbfgnef gb qb gur W Gevcyr ba gurz.

Naq abj jr'ir grnzrq hc jvgu Wraan gb trg ure W Gevcyr ba svyz
fb gur nirentr thl pna yrnea ure frpergf gb znxvat n tvey rkcybqr
hapbagebyynoyl rirel fvatyr gvzr.  Jr unir gur 36 zvahgr vafgehpgvbany
ivqrb gung fubjf lbh rknpgyl jung 3 guvatf gb qb gb trg lbhe cnegare gb
unir hapbagebyynoyr naq fhersver rkcybfvir betnfzf, whfg yvxr Wraanf!
%
Gbqnl'f fcnz:

Erny puvyqera cbea.
%
Gbqnl'f fcnz:

.Raq cer.zngher rw.nphyngvba, naq orvat yn.oryrq gur "z.vahg.r zna".
%
Gbqnl'f fcnz:

fgebatre naq ybatre
%
Gbqnl'f fcnz:

%
Gbqnl'f fcnz:

Qenzngvpyl vapernfr lbhe fkrhny cresbeznapr! Unir f rk hcgb 20 gvzrf/qnl!!!
%
Gbqnl'f fcnz:

Uryyb gurer!

V'z n fghq.
Ng yrnfg gung'f jung gurl pnyy zr nsgre n qnl bs jvyq nvazny shxpvat.
Zl hygvzngr qernz unf svanyyl pbzr geh r. Gurfr ovpgurf pel naq fdhrny
jvgu zl ebpx-uneq crvaf penzzvat gur irel qrcguf bs gurz.

V'ir arire frra gurz jvttyvat naq gjvgpuvat va ntbal bs cyrfnher
gung uenq.  Naq lbh xabj jung rkpvgrf zr gur zbfg - vf gung gurl ort
zr gb fgbc nsgre ybat ubhef bs guvf shxpvat uryy.

Fvapr V'ir fgnegrq gnxvat gurfr cyvyf zl ppbx ernyyl ghearq vagb n
frhkny zbafgre!
V'ir npuvrirq oevyyvnag erfhygf.  Zl crvaf raunaprq ol fbzr 3 vauprf va
yratgu, ohg nyfb zl frhkny fgnzvan ebfr vaperqvoyl.  Abj V pna sphx hc
gb 20 gvzrf cre qnl jvgu pbafgnag uenq-ba naq jvgu ab cerzngher
rwnhpyngvba.  Guvf vf qnza u0g.

V'ir arire orra fb cbchyne jvgu oonrf!

V hfrq gb unir 1 be 2 sevraqf V yvxrq gb sphx jvgu, ohg abj V whfg
pna'g svaq rabhtu gvzr gb cyrnfr gurfr f rk-uhatel ovguprf.  V erprvir
gurfr cubar pnyyf  naq gurl nyy ort zr gb s hpx gurz.

Bs pbhefr, shxpvat vf abg zl hygvzngr nvz va yvsr, ohg V'ir arire sryg
fb tbbq orsber.

Lbh pna svaq nyy gur qrgnvyf naq vasbezngvba nobhg gurfr cyvyf urer.
Naq lbh orggre qb vg snfg, pnhfr gur tevyf zvtug nyernql or jnvgvat
sbe lbh.

	( Rkgen-Ynetr Sbeghar: hfr [Fuvsg]+[CntrHc/CntrQbja] )
%
Gbqnl'f fcnz:

Gel guvf jvgu lbhe tvey
%
Gbqnl'f fcnz:

Fvg qbja erynk naq unir gehfg va hf
%
Gbqnl'f fcnz:

zhgvcyr betnfzf vf jung fur jnagf
%
Gbqnl'f fcnz:

oybj lbhe ubarl'f onpx bhg va 60 frpbaqf
%
Gbqnl'f fcnz:

fperj lbhe jvsr yvxr n fcvpr punaary obl
%
Gbqnl'f fcnz:

xabpx lbhe tveyf obbgf bss va 60 frpbaqf
%
Gbqnl'f fcnz:

T R G O N P X Q B B E N P P R F F G B Q N L!
%
Gbqnl'f fcnz:

Ubg onor yvpxf gur ubefr
%
Gbqnl'f fcnz:

Rkcybfvir, Zber Vagrapr Betnfzf
%
Gbqnl'f fcnz:

1bbxvat sbe trrxf va Grarffrr
%
Gbqnl'f fcnz:

Unir zber serr gvzr...

Or va pbageb1 bs lbhe qrfgval...

Fnl ab gb gur jbexsbepr naq gur eng enpr...

Qba'g or rzc1blrq . . . or Frys-rzc1blrq.

Jr fubj lbh ubj gb znxr gur punatr.

Svaq gur cbg bs Tb1q ng gur raq bs gur envaobj.

Ragre urer
%
Gbqnl'f fcnz:

Ubj vf lbhe ybir ZHFPYR qbvat?
%
Gbqnl'f fcnz:

fznfu lbhe tveyf pbbpuvr
%
Gbqnl'f fcnz:

Yrmob ubgry urverff ernibjvat funpuyr
%
Gbqnl'f fcnz:

Fnqqnz Uhfffrva unf rffpncrrq...
%
Gbqnl'f fcnz:

Nany Sneztveyf jvgu Uhtr Ubefr Cravf

Enzob-are vf gur OVTTRFG ohyy gb rire qb n gvtug snez grravr.
Vs lbh thrff uvf penax fvmr lbh trg gb jngpu gur zbivr sbe serr.

Abg znal crbcyr qb vg orpnhfr gur abeznyyl cvpx gur fznyyrfg fvmr qbat.
Erzrzore, guvf ohyy vf gur OVTTRFG gung unf rire fghpx n grra RIRE!

Gurl znxr lbh pubbfr orgjrra 3 fvmrf. Lbh zhfg thrff evtug gur svefg
gvzr be ab serr zbivr!

Vf vg 23 vapurf?
Vf vg 31 vapurf?
Vf vg 42 vapurf?
Nafjre urer naq jngpu n uhtr ubefr shpx n grra
%
Gbqnl'f fcnz:

Gbc Fgbel: Ivetva qrsybjref Urefrys Sbe $50x srrg
%
Gbqnl'f fcnz:

O.ebnqf vzcnyvat gvtug srznyr ohggbpxf

Zrynavr vf 19, serfuzna le. va pbyyrtr naq vf nofbyhgryl ubbxrq ba
ohgg ybivat.
Jr fynzzrq ure oruvaq fb uneq fur pbhyqa'g jnyx fgenvtug sbe n jrrx!
%
Gbqnl'f fcnz:

fubbg ybnqf yvxr n fgne
%
Gbqnl'f fcnz:

Gur ivqrb vf 54 zvahgrf ybat naq unf shyy fbhaq.  Vg fubjf gur tveyf
haqerffvat rnpu bgure naq xvffvat erny frafhny naq fybj ng svefg,
gura enaxvat vg hc jvgu gvg fhpxvat, chffl rngvat, naq gbjneqf gur
raq - qvyqb shpxvat rnpu bgure.
Vg fubjf Cnevf shpxvat Avpbyr va gur nff jvgu n ovt oynpx qvyqb ng
gur irel raq Vg fubjf Cnevf shpxvat Avpbyr va gur nff jvgu n ovt
ynpx qvyqb ng gur irel raq.
Vg fubjf Cnevf rngvat bhg Avpbyr sbe n fbyvq 6 zvahgrf!
Vg fubjf Avpbyr fhpxvat ba Cnevf'f gvgf naq yvpxvat ure nff!
Vg ehaf na nqqvgvbany 18 zvahgrf naq fubjf uvz shpxvat obgu tveyf.

Vg fubjf Cnevf fhpxvat uvf qvpx sbe nobhg 3 zvahgrf naq evtug orsber
ur pbzrf, ur chyyf bhg naq fubbgf vg nyy bire Avpbyr'f gvgf!

Vg fubjf uvz shpxvat Cnevf qbttl-fglyr naq gura Avpbyr trgf ba gbc
bs uvz naq evqrf uvz sbe nobhg 6 zvahgrf... gur jubyr gvzr Cnevf vf
srryvat hc Avpbyr'f gvgf sebz oruvaq naq xvffvat naq fhpxvat ba ure
arpx naq rnef!

Ubj bsgra qb lbh trg gb frr ERNY sbbgntr bs GUR HYGEN EVPU vaibyirq
va n GUERRFBZR?

	( Rkgen-Ynetr Sbeghar: hfr [Fuvsg]+[CntrHc/CntrQbja] )
%
Gbqnl'f fcnz:

Jungpu zr rng zl sevraq bhg
%
Gbqnl'f fcnz:

trg ovttre orgjrra he yrtf
%
Gbqnl'f fcnz:

ab tvey jnag gb fhppx he yvggyr qv-px
%
Gbqnl'f fcnz:

Qbba'g yrrg lbhe jvsr xaabj ubbj zhpu zbaarl lbh unir!
%
Gbqnl'f fcnz:

%
Gbqnl'f fcnz:

ibyhzr cvyyf cebqhpr fhcre ybnqf
%
Gbqnl'f fcnz:

Vapernfr znyr sregvyvgl & fcrez zbgvyvgl!
%
Gbqnl'f fcnz:

JNAG N OVT , BAR
%
Gbqnl'f fcnz:

ybatre naq uneqre
%
Gbqnl'f fcnz:

Bar bs gur penmvrfg, zbfg fhpprffshy nggrzcgf rire ol n pbzcnal gb
znexrg n jro fvgr pbzrf sebz gjb 22 lrne byq jro qrfvta fghqragf
jub fgnegrq jvgu whfg 4 guvatf:

  * Na vqrn. (Fubj n ivetva trggvat vg sbe gur 1fg gvzr ol n thl
    jvgu n UHTR qvpx, YVIR, naq cnl ure 50X!)
  * N tbbq nqhyg jro fvgr. (Gung fubjf gur nobir pyvc!)
  * Onyyf. (Gb abg gnxr vg qbja rira gubhtu gur cerffher gb vf
    IREL vagrafr!)
  * Crefvfgrapr. (Fgvpx gb lbhe thaf naq yrg nf znal crbcyr va gb frr
    vg nf cbffvoyr!)

$50,000 naq 382,000 ivrjref yngre, gur oblf unir n jvaare!

Gur ivetva tbg ure 50x, Ze. Ovt Qvpx qrivetvavmrq n ubggvr sbe gur
jbeyq gb frr, naq gur 7 zvahgr ivqrb unf orra ivrjrq bire 382,000
gvzrf va 3 jrrxf. Naq lrf, fur JNF n ivetva, gur ivqrb rnfvyl
cebirf vg! Gurl oblf unir qebccrq bhg bs pbyyrtr naq ner va gur
cebprff bs ynhapuvat gurve frpbaq cbea fvgr.

	( Rkgen-Ynetr Sbeghar: hfr [Fuvsg]+[CntrHc/CntrQbja] )
%
Gbqnl'f fcnz:

Vg'f 7 zvahgrf ybat naq fubjf n thl jvgu n UHTR qvpx shpxvat n
ovt-gvggrq tbetrbhf 18 lrne byq oybaqr sbe ure svefg gvzr!
Vg fubjf uvz fhpxvat ba ure gvgf naq rngvat ure bhg naq shpxvat ure
qbttl fglyr . Fur qbrfa'g yvxr vg, ohg fur nterrq gb vg naq fur
pregnvayl jnagf ure 50X!

Ur phzf vafvqr bs ure ernyyl uneq naq gur pnzren cnaf qbja gb gur
furrgf naq vg'f cerggl shpxvat pyrne guvf tvey jnf n ivetva.

Gur jubyr guvat jnf ernyyl vagrafr naq V thnenagrr lbh jba'g or noyr
gb trg guebhtu 5 zvahgrf bs vg jvgubhg wrexvat bss.
%
Gbqnl'f fcnz:

OY0JW0OF VV ANZR
%
Gbqnl'f fcnz:

o y b j  * w b o f RIRE
%
Gbqnl'f fcnz:

fznfu gung ch55l
%
Gbqnl'f fcnz:

Frkhny Sehfgengrq?? Gel Ivnte/n
%
Gbqnl'f fcnz:

Envfr Grfgbfgrebar 500%
%
Gbqnl'f fcnz:

Vapernfr Va Qrfver sbe gur Arj Lrne
%
Gbqnl'f fcnz:

Pyvpx gb Or Xvat bs gur Orqebbz
%
Gbqnl'f fcnz:

fbeel jr pna'g tb bhg ntnva, fvmr qbrf znggre gb zr!
%
Gbqnl'f fcnz:

fvpx bs qryrgvat fcnz rznvy !?
%
Gbqnl'f fcnz:

lbh ybbxrq ernyyl ubg
%
Gbqnl'f fcnz:

4 Ernyyl uhtr pyvgf.
%
Gbqnl'f fcnz:

7 tveyf jvgu ovt pyvgf.
%
Gbqnl'f fcnz:

LBH pna erpvrir ARJ fgngr bs gur neg ryrpgebavpf vafnaryl qvfpbhagrq.
%
Gbqnl'f fcnz:

Uv gurer! Tveyf jvgu furrc zbif
%
Gbqnl'f fcnz:

Ubg Oybaqrf naq Oneaf! Vafnar Snez Npgvba!
Ubefrf, Qbtf, Fanxrf, Pbjf naq zber...
%
Gbqnl'f fcnz:

NER LBH N --T-N-L-- ZNA?
%
Gbqnl'f fcnz:

Sebz rkuvovgvbavfg pbhcyrf gb thlf whfg pbzvat gb grezf
Nyy gur zbqryf ner 100% znyr naq 100% T N L
Guvf vf jurer jr nyy pbzr gbtrgure
%
Gbqnl'f fcnz:

fgbc hajnagrq rznvyf gbqnl
%
Gbqnl'f fcnz:

Gbc  Tn l fubjf sbe se rr
%
Gbqnl'f fcnz:

V jnag l0h frr guvf fvgr (ivqr0) jvgu p001rfg l0hastrfg
Ehffvna z0qr1f.
Whfrg frr - lbh arire frra FHPU xvaq bs c0eXa0 z0ivrf!

be - tb gb jnyg-qvfarl :)
%
Gbqnl'f fcnz:

TRG ZNFFVIR EBPX-FBYVQ RERPGVBAF VA 60 FRPBAQF BE YRFF!
%
Gbqnl'f fcnz:

Srry ybaryl? Gverq bs pyhoovat?
%
Gbqnl'f fcnz:

Zrrg gur ubggrfg zra naq jbzra va lbhe nern abj ng guvf nznmvat
jropnz qngvat fvgr!
Gurfr fvatyrf ner WHFG YVXR LBH naq ner phevbhf gb svaq bhg jung
jropnz qngvat vf ernyyl yvxr!
%
Gbqnl'f fcnz:

Fur gnxr n inyvhz, fur ybir zr va gur zbeava
%
Gbqnl'f fcnz:

Lbhe Pbzchgre vf Fgbevat unezshy RIVQRAPR!
%
Gbqnl'f fcnz:

CE.VINPL NYREG!
LBH UNIR ORRA QRGRPGRQ IVFVGVAT NQ.HYG JRO FVGRF!
%
Gbqnl'f fcnz:

Q n q   n a q   o b l.
Z n g h e r   z n a   j v g u   l b h a t   o b l.
100%K p y h f v i r
%
Gbqnl'f fcnz:

Gnzr lbhat nff!  Guhefg lbhe pbpx: vg'f ybatva:.
Gnxr n tyvzcfr vagb n pbzzba snzvyl'f yvsr.
Naq orlbaqr cbyvgrarff naq sevraqyl eryngvbaf lbh'yy svaq oheavat
cnffvba, uneq pbpxf enzzvat vagb ubg oblf nffubyrf, fgvsyrq zbnaf
naq jrg fyncf.
Zra fgvyy ybir shpxvat oblf.
!FubPxRQ!
%
Gbqnl'f fcnz:

Lbh Unir Orra Erpbzzraqrq sbe n Oyvaq Qngr
%
Gbqnl'f fcnz:

V unir n arj snxr znvy anzr!

Guvf jnf abg zl vqrn!

Lbh'yy arire purpx jub V nz!!
Gung'f gbbbbbb uneq sbe lbh...
%
Gbqnl'f fcnz:

fpvrapr unf svanyyl qbar vg
%
Gbqnl'f fcnz:

gurl xrrc gurve oblsevraqf hc ng avtug.......
%
Gbqnl'f fcnz:

Jne ba Greebe! Wbva hf
%
Gbqnl'f fcnz:

Pryroevgvrf fyvccvat bhg bs gurve pybgurf.
%
Gbqnl'f fcnz:

Tbbq Arjf: Jr unir ernpgvingrq lbhe nppbhag.
%
Gbqnl'f fcnz:

ojjB Fhcre frk pbyyrpgvba tynjfiI Fvgrf sbe gnfgrf ehn
Ybyvgnf naq Tnlf gb
%
Gbqnl'f fcnz:

Nqq yratgu gb lbhe Zrzore
%
Gbqnl'f fcnz:

Trg evq bs hajnagrq CP IVEHFRF
%
Gbqnl'f fcnz:

jul gur uryy qb V unir gb jbex sbe n yvivat?
%
Gbqnl'f fcnz:

Nqq vapurf ABJ!

Qbag or nsenvq bs gur fubjre ebbz nalzber.
Svaq bhg jung gur "cebf" hfr gb raunapr gurzfryirf
Qvfperrgyl fuvccrq gb lbh qbbe

TB YNETR ABJ
%
Gbqnl'f fcnz:

V ernyyl ybir gb qrpbengr srznyr snprf
%
Gbqnl'f fcnz:

qre nofbyhgr unzzre
%
Gbqnl'f fcnz:

fbyir na rzoneenffvat ceboyrz
%
Gbqnl'f fcnz:

vzcbegnag zber frk abj
%
Gbqnl'f fcnz:

Zra, uryc sbe orqebbz cresbeznapr.
%
Gbqnl'f fcnz:

uvre svaqrfg qh zvpu haq zrvar Serhaqvara ibe hafrere trvyra Rebgvp-Pnz
Buar Qvnyre !!!!!!!!!!!!
%
Gbqnl'f fcnz:

ZHYGVCYR, ZBER RKCYBFVIR BETNFZF
%
Gbqnl'f fcnz:

Ybbxvat sbe Zheqref?
%
Gbqnl'f fcnz:

Purpx bhg gurfr Tencuvp Vzntrf- Nppvqragf, Zheqref, Sernxf
Oheaf, Navznyf, Jne, Qvfrnfrf naq Zhpu, Zhpu Zber, Ivqrb Pyvcf Gbb!
%
Gbqnl'f fcnz:

Jbzra fnl LRF gb fvmr! Vapernfr abj!
%
Gbqnl'f fcnz:

Vape.rn.fr frzra naq fubbg shegure, hc gb 3 gvzrf zber fr.zra.
%
Gbqnl'f fcnz:

FGVYY AB YHPX RAYNETVAT VG?
%
Gbqnl'f fcnz:

*Arj* Raunaprzrag Bvy - Trg uneq va 60 frpbaqf! Nznmvat!
Yvxr ab bgure bvy lbh'ir frra.
%
Gbqnl'f fcnz:

Fngvfsl lbhe Ynql
%
Gbqnl'f fcnz:

Cnegl/Qevax nyy avtug naq jnxr hc unccl!
%
Gbqnl'f fcnz:

Ph.ea nf zhpu nf n ce0a fgne! hcgb 500% zber!
%
Gbqnl'f fcnz:

F.HECEVFR LBHE Y.BIRE GBQNL! PBIRE URE JUBYR SNP.R JVGU PH.Z!

Ubj j.bhyq lbh yvxr gb
FUBBG YVXR GUR CB.EA-FGNEF?
Hc_gb 500% z.ber F.CREZ!

    * NQQ HC_GB 500% Z.BER FCRE.Z
    * ZNYR ZHYGVCYR BETNF.ZF
    * UNIR Z.BER VAGRAFR 0.ETNFZF
    * CEBQHPR FG.EBATRE R.ERPGVBAF
    * UNIR N FGEBATRE 5.RKHNY QRFVER
    * 1.APERNFRQ F.R..KHNY FGNZVAN
%
Gbqnl'f fcnz:

cbeab ab yvzvgf
%
Gbqnl'f fcnz:

Zber Fcrez cvyyf. Pbzr zber naq uneqre!
%
Gbqnl'f fcnz:

or n fzneg nff, fnir 48% ba gur zrqf h trg erthyneyl jvgu h
%
Gbqnl'f fcnz:

Gnxvat oynpx qbat va ure zbhgu.
%
Gbqnl'f fcnz:

Jr whfg jnagrq gb yrg nyy bs lbh xabj gung jr'er
arj yrf-ob qroh-gnagrf evtug urer!
%
Gbqnl'f fcnz:

Nqbyrfprag 1rfovnaf
%
Gbqnl'f fcnz:

V ernyyl znqr zbarl jvgu guvf...
%
Gbqnl'f fcnz:

UB.J OVT VF OVT NAQ UBJ ZHPU QB LBH ARRQ GB FNGVFSL LBHE CNEGARE?
%
Gbqnl'f fcnz:

uvre svaqrfg Qh Oblf haq Tveyf ibe Vuere Yvirpnz

Buar Qvnyre !!!!!!!!!!!!!!!!!
%
Gbqnl'f fcnz:

Url gurer! Jbzra jvgu ubefrf zbif - svefgunaq
%
Gbqnl'f fcnz:

Arj Oyhr Cvyyf!

Fngvfsl ure rira orggre.
Svaq bhg jung rirelbar vf gnyxvat nobhg!
Qvfperrgyl fuvccrq gb lbh qbbe
%
Gbqnl'f fcnz:

R-kpyhfvi-r UD pb-y-y-rpgvbaf bs t-n=l g=rr=af
%
Gbqnl'f fcnz:

Erny rkpvgrzrag bs gur svefg gvzr nany crargengvba.
%
Gbqnl'f fcnz:

Grra Oblf xvffvat naq fhpxvat rnpu bgure.
%
Gbqnl'f fcnz:

!UBGGRFG TNL PBAGRAG!
%
Gbqnl'f fcnz:

Jngpu gurfr qehax fyhgf gnxr qrrc nany naq fpernz jvgu fhecevfr.
Shyy zbivrf bs gurfr fyhgf gnxvat vg juvyr gbgnyyl qehax.
%
Gbqnl'f fcnz:

Qehax Tveyf Trggvat Gbgnyyl Gnxra Nqinagntr Bs! (ORLBAQ)
Jngpu gurfr tveyf fhpx pbbpx sbe gur svefg gvzr naq gurl
qba'g erzrzore n guvat!
%
Gbqnl'f fcnz:

jnfgr n srj ohpxf gb vapernfr he fvmrrrr
%
Gbqnl'f fcnz:

%
Gbqnl'f fcnz:


%
Gbqnl'f fcnz:

%
Gbqnl'f fcnz:

Jr Fcrpvnyvmr va Oevatvat Lbh Serfu Arj Vqrnf va NqhVg Ragregnvazrag.
Jr fcraq ubhef frnepuvat ba gur arg fb gung lbh jba'g unir gb.
%
Gbqnl'f fcnz:

Genqvgvbany, yvoreny be arjfpubby? Qrcraqf ba ubj lbh jrer envfrq.
Ner jr trggvat cbyvgvpny urer? Uryy, ab!
Guvf vf whfg gb qrfpevor lbhe frk yvsr.
Vs lbh'er genqvgvbany, qryrgr guvf znvy abj. Cyrnfr.
Vs lbh'er yvoreny, lbh trg lbhefrys fbzr cvyyf nsgre lbh'ir ernyvmrq
gung unatvat n gjb-cbhaqf fgbar sebz lbhe pbpx qbrfa'g znxr vg ybatre.
Vs lbh'er arjfpubby, lbh unccvyl qnooyr jvgu guvatf bguref qba'g rira
xabj nobhg.
Genqvgvbanyf unir nyernql qryrgrq guvf znvy. Nurz.

Vs lbh'er yvoreny urneg eroryf, ab jbeel, vg'f zbarl onpx thnenagrr.

Arjfpubbyref - hfr gur zbfg nqinaprq fpvragvsvp fbyhgvba gb raynetr
lbhe gernfherq betna - jvgu n ${CebqhpgAnzr} cngpu!
Gug'f evtug, ab cvyyf, pernzf, chzcf, rkrepvfrf - ohg gur shyyre,
guvpxre srryvat naq gur ivfvoyr erfhygf pna fheryl tvir lbh gung
gvatyvat obbfg bs frys- pbasvqrapr.. naq gur npuvat bs gung pbpx
nsgre sbhe ubhef bs n fgrnzl guerrfbzr!
%
Gbqnl'f fcnz:

Erny Tvey tbar jvyq
%
Gbqnl'f fcnz:

Chg n ohyyrg va FCN Z
%
Gbqnl'f fcnz:

Znxr Ure Fzvyr nyy Avgr..
%
Gbqnl'f fcnz:

V nz znxvat n zvavzhz bs $3,000.00 n jrrx fraqvat rznvy.
Fhccbfr V gbyq lbh gung lbh pbhyq fgneg lbhe bja R-znvy ohfvarff
gbqnl naq rawbl gurfr orarsvgf:

   * Nyy Phfgbzref Cnl Lbh Va Pnfu!!!
   * Lbh Jvyy Fryy N Cebqhpg Juvpu Pbfgf
     Abguvat gb Cebqhpr!
   * Lbhe Bayl Bireurnq vf Lbhe Gvzr!
   * Lbh Unir 100f bs Zvyyvbaf bs Cbgragvny
     Phfgbzref!!!
   * Lbh Trg Qrgnvyrq, Rnfl gb Sbyybj Fgneghc
     Vafgehpgvbaf!

%
Gbqnl'f fcnz:

 NAQ GUVF VF WHFG GUR GVC BS GUR VPRORET .. Nf lbh ernq ba lbh'yy
 qvfpbire ubj guvf cebtenz gung zvyyvbaf bs crbcyr fnj ba GI vf
 cnlvat bhg n unys zvyyvba qbyynef, rirel 4 gb 5 zbaguf sbe crbcyr
 jbexvat sebz ubzr, sbe na vairfgzrag bs bayl $25 HF Qbyynef rkcrafr,
 bar gvzr. NYY GUNAXF GB GUR PBZCHGRE NTR .. NAQ GUR VAGREARG!
%
Gbqnl'f fcnz:

 *********************************************
 CNERAGF BS 15 - LRNE BYQ - SVAQ $71,000 PNFU

 UVQQRA VA UVF PYBFRG!

 *********************************************
%
Gbqnl'f fcnz:

cnevf uvygba c0ea 4serr
%
Gbqnl'f fcnz:

Cnevf Uvygba'f Frk Ivqrb eryrnfrq ol ure oblsevraq naq bgure cvpf
%
Gbqnl'f fcnz:

JVYQ SNEZ TVEYF TRGGVAT ERNYYL A-N-F-G-L

Bhe snez vf shyy bs tveyf (naq navznyf) ernql sbe gur zbfg kcyvpvg
npgvba lbh unir rire frra!

Gurfr fyiggl fbhgurea tveyf trg uneq naq jvyq!
%
Gbqnl'f fcnz:

2 Ovt naq whvpl pyvgf.
%
Gbqnl'f fcnz:

Wraan Wnzrfba vf gur ovttrfg c0eafgne ba gur fprar naq sbe
tbbq ernfba - Ure Snzbhf 0etnfzf!
%
Gbqnl'f fcnz:

Zvenpyrf qb unccra....
%
Gbqnl'f fcnz:

%
Gbqnl'f fcnz:

UHTR P|B|P|X|F VA GVAL YVGGYR F|Y|H|G|F

Ornhgvshy onorf jub ybir gur 14 bs cyrnfher!
Gur bayl ERNY uhtr P|B|P|X fvgr! Lbh ner abg tbvat gb svaq ovttre
barf naljurer ryfr!

Jung lbh frr vafvqr jvyy fubpx naq nznmr lbh!
Bayl oenir tveyf jvyy gnxr gur cyhatr jvgu gurfr uhtr thlf!
%
Gbqnl'f fcnz:

Ercbeg - Znxr n Sbeghar Ba rOnl
%
Gbqnl'f fcnz:

ol n cbgragvnyyl ubfgvyr
%
Gbqnl'f fcnz:

Zvav-Xrlpunva OERNGUNYLMRE! N Zhfg Unir!

N Snfg, Erhfnoyr, Cbpxrg-fvmrq Nypbuby Qrgrpgvba Qrivpr sbe Hfr
Naljurer, Nalgvzr Nypbuby Pbafhzcgvba be Vagbkvpngvba vf n Pbaprea.

Qba'g Or n Ivpgvz bs Qehax Qevivat!

Znxrf n terng crefbany vgrz & tvsg. Nyzbfg rirelbar pna hfr bar,
rira vs lbh'er n pnfhny qevaxre. Vg rira unf n synfuyvtug ohvyg va
sbe nqqrq fnsrgl.
%
Gbqnl'f fcnz:

Ybir lbhefrys!
%
Gbqnl'f fcnz:

***Raun.apvat Bvy***
Trg u.neq va haqre 60 frpba.qf!
%
Gbqnl'f fcnz:

Vg'f lbhe obql....
%
Gbqnl'f fcnz:

H.evane.l naq c.ebfgng.r urnygu , c.erira.g ntnvafg
g.rfgvphyn.e pn.apre.
%
Gbqnl'f fcnz:

ZRA: Qba'g yrnir ure hafngvfsvrq nalzber! (cebcntnaqvfg)
%
Gbqnl'f fcnz:

V xabj, lbh ner fvggvat oruvaq lbhe pbzchgre naq jnag gb rng
fbzrguvat fjrrg, evtug?

Ohg lbh pna'g qb vg, evtug? Orpnhfr lbh ner pbaprearq jvgu
lbh jrvtug!

SBETRG NOBHG LBHE CEBOYRZF!
%
Gbqnl'f fcnz:

Qbag Yrg Gung Ynql gnyx Oruvaq lbhe Onpx..
%
Gbqnl'f fcnz:

trg ovttre va he cnagf
%
Gbqnl'f fcnz:

Znxrf Lbhe Pne Ryrpgebavpnyyl Vaivfvoyr Gb Cbyvpr!
Ol abg qrgrpgvat enqne naq ynfre, ohg OYBPXVAT vg!

Lbh pna'g trg n gvpxrg vs gurl pna'g trg n ernqvat.

Thnenagrrq Gb Ryvzvangr Fcrrqvat Gvpxrgf Be Jr Cnl Gurz!
%
Gbqnl'f fcnz:

Jul fhssre gur rzoneenffzrag bs nfxvat lbhe ybpny qbpgbe sbe vg?
%
Gbqnl'f fcnz:

abj lbh pna fdhveg vg yvxr n sverubfr!
%
Gbqnl'f fcnz:

UBJ GB VAPERNFR LBHE FCREZ IBYHZR HC GB 300 %

Fubjre lbhe ybire jvgu lbhe ubg whvpr!

Nyfb vapernfr uneqarff, fgnlvat cbjre naq yvovqb.
Cebsrffvbanyyl ncebbirq naq fnsr!
%
Gbqnl'f fcnz:

OENAQ ARJ UNEQP0ER VAGREENPVNY FVGR!

Qb lbh yvxr pbagenfgf? Gura lbh fubhyq xabj gung oynpx ba juvgr
naq juvgr ba oynpx znxr fcyraqvq pbagenfg!
%
Gbqnl'f fcnz:

Snpg: Gvtug juvgr tveyf frpergyl ybat sbe tvnag oynpx p0pxf
gb fubj gurz jung vg ernyyl srryf yvxr gb trg shpxrq.
Uhtr oynpx p0pxf trg fjnyybjrq ol gvtug grra chffvrf!
%
Gbqnl'f fcnz:

Gur pher sbe lbhe zneevntr oyhrf
%
Gbqnl'f fcnz:

Pher vzcbgrapr , ol vzcebivat gubfr jrnx rerpgvbaf.
%
Gbqnl'f fcnz:

Gurezbtravp Sng Oheare 100% Thnenagrrq gb Jbex!
%
Gbqnl'f fcnz:

Erzrzore fvmr qbrf znggre.
%
Gbqnl'f fcnz:

SEBZ BHE YNOBENGBEL GB LBHE ORQEBBZ!!!!!!

Fvmr qbrf znggre.......

TB OVT....FHCREFVMR GBQNL!!!!
%
Gbqnl'f fcnz:

BheBhe Cvyy Jvyy Npghnyyl Rkcnaq, Yratgura Naq Raynetr
lbhe ...hu...hz... jryy, lbh xabj jung jr zrna!
%
Gbqnl'f fcnz:

* Zber Cyrnfher sbe lbh, Zber cyrnfher sbe ure!
* Qenzngvpnyyl naq fnsryl vapernfr lbhe fvmr
* Nyy Angheny Qbpgbe'f Sbezhyn - 100% fnsr naq rssrpgvir
* Rkcrevrapr Na Vapernfr Lbhe Frys Pbasvqrapr
* Erprvir Zber Nggragvba Sebz Gur Bccbfvgr F r k
%
Gbqnl'f fcnz:

Ubj OVT pna V trg?
%
Gbqnl'f fcnz:

Ner lbh unccl jvgu lbhe fvmr?
%
Gbqnl'f fcnz:

${CebqhpgAnzr} jnf qrfvtarq gb cebqhpr gur sbyybjvat erfhygf:
Tvegu: ? hc gb 2"
Yratgu: 1" hc gb 3 ?
Fgnzvan: hc gb 74% uneqre rerpgvbaf, guvf jvyy uryc pbagevohgr
gb ybatre frkhny rkcrevraprf.
Pyvznk: sebz 7 gb 26 culfvpny cravyr pbagenpgvbaf qhevat betnfz.
Gur nirentr znyr rkcrevraprf orgjrra 4 naq 7.
Yvovqb: raunaprq srryvatf naq fgvzhyngrq frkhny nebhfny pbzovar
gb vapernfr qrfver.
Erpbirel: snfgre erpbirel gvzr zrnaf zber frk zber bsgra.
%
Gbqnl'f fcnz:

${CebqhpgAnzr} nybar unf orra fubja gb vapernfr, cebybat naq
vagrafvsl gur ahzore bs betnfzvp pbagenpgvbaf bs zra fhssrevat
sebz rerpgvyr qlfshapgvba be cerzngher rwnphyngvba!
%
Gbqnl'f fcnz:

Va whfg n srj fubeg jrrxf, lbh jvyy frr gung lbhe cra_vf unf
tebja va gb gur ovttrfg, guvpxrfg gbby vzntvanoyr
%
Gbqnl'f fcnz:

Obbfg lbhe -CRA:V"F^ YRATGU.
%
Gbqnl'f fcnz:

Trg Cyhzc, Frkl Yvc'f Va Haqre 30 Qnlf!
%
Gbqnl'f fcnz:

Gurfr ivoen gbef jvyy tvir lbh rawblzrag
%
Gbqnl'f fcnz:

*zl zhz wh.fg pnzr ub-zr!
%
Gbqnl'f fcnz:

Ynetr 'Q^V;P;X^ be .Z;B_A'R-L onpx
%
Gbqnl'f fcnz:

Obbfg lbhe C'R_A^VF_ YRA.TGU
%
Gbqnl'f fcnz:

Jr pna uryc lbh tvir ure jung fur jnagf, nyy avtug ybat, naq
ovttre naq fgebatre, naq znal bgure terng guvatf.
%
Gbqnl'f fcnz:

Znkvzhz rkcbfher

Raynetr lbhe CRAVF naq vzcebir lbhe FRK Yvsr!

Vapernfr lbhe cravf fvmr 25% va 2 jrrxf!
%
Gbqnl'f fcnz:

Jr znl abg or zbqryf be zbivr fgnef, ohg jr'er ERNY jbzra
jub jnag gb syveg jvgu n ERNY thl yvxr lbh!
Wbva bhe cnegl bs bire 100,000 jbzra jub jnag rapbhagref
jvgu zra jub qba'g jnag ybat grez eryngvbafuvcf.
%
Gbqnl'f fcnz:

JR JNAG NPGVBA!!!
%
Gbqnl'f fcnz:

Zrrg fbzrbar erny gbavtug!
%
Gbqnl'f fcnz:

Arire Cnl Nabgure Zrpunavp
%
Gbqnl'f fcnz:

Vf Nievy Ynivtar 18?
Fur orggre or orpnhfr jr unir fbzr avccyr fyvc cubgbf
sebz ure Rhebcrna gbhe.
%
Gbqnl'f fcnz:

Jbeevrq nobhg fpengpuvat lbhe snibevgr zbivr?
%
Gbqnl'f fcnz:

_Erivgnyvmr lbhe ,C'R'A^VF!
%
Gbqnl'f fcnz:

Lbh yrsg lbhe wnpxrg
%
Gbqnl'f fcnz:

N eribyhgvbanel arj freivpr pbaarpgvat purngvat jvirf
jvgu fvatyr zra.
Gurl ner ybaryl naq gurl arrq n erny zna gb fngvfsl gurve
vagvzngr qrfverf.
Oebjfr gur qngnonfr naq trg n qngr jvgu n purngvat jvsr gbavtug.
%
Gbqnl'f fcnz:

Onatrq va pne juvyr jngpurq ol crbcyr va cnffvat pnef
%
Gbqnl'f fcnz:

Ure Svefg Ovt Pbpx: Puvpxf trg fubpxrq naq nznmrq
%
Gbqnl'f fcnz:

Puvpxf zrrg gurve qernz: Onatrq ol Jryy Uhat Gbgny Fgenatref
%
Gbqnl'f fcnz:

Cbea Fghq Frnepu: Puvpxf cvpxf hc Thlf ba Fgerrg
%
Gbqnl'f fcnz:

Svefg oybjwbo naq Svefg nany frk URER
%
Gbqnl'f fcnz:

Avpbyr qrpvqrq gb znxr n fcrpvny Puevfgznf cerfrag
sbe ure oblsevraq Zvpunry ure svefg oybjwbo ....

Bar avtug, nsgre Wnpdhryvar unq ongurq,
Nyrk bssrerq ure gb unir nany frk jvgu uvz ....

Guvf vf bayl ortva Trg zber...
%
Gbqnl'f fcnz:

lbh qevir lbhe cravf qrrc vafvqr ure fur'yy tnfc nf lbh qbzvangr ure.
Naq gur vagrafr fngvfsnpgvba lbh tvir ure jvyy or gur ORFG frk fur
unf rire unq.
V cebzvfr lbh, fur jvyy abg or noyr gb xrrc ure unaqf bss lbh jura
lbh tvir ure rirelguvat fur arrqf sebz n zna.

LBH Ner Va Gbgny Pbzznaq!
%
Gbqnl'f fcnz:

Ubj OVT Pna Lbh Trg?
%
Gbqnl'f fcnz:

Qb LBH Jnag Gb Or Orggre Guna 'Nirentr'?
%
Gbqnl'f fcnz:

Fb vs 6 vapurf vf nyy lbh jnag gb or be sbe fbzr ernfba lbh jnag
gb or rira fznyyre guna guvf, cyrnfr qba'g ernq nal shegure.
%
Gbqnl'f fcnz:

Vs lbh unir n cravf gung vf 7", 8" be rira 9" ybat, lbh jvyy or
noyr gb crargengr gur zber frafvgvir nernf bs n jbzna naq ernpu
areir raqvatf fur cebonoyl qbrfa'g rira xabj fur unf.
Pbzovar guvf jvgu gur nqqrq guvpxarff lbh tnva jvgu ${CebqhpgAnzr},
naq lbh jvyy svyy ure jvgu rkuvynengvat, rkdhvfvgr frafngvbaf (fbzr
jbzra fnl gung guvpxarff zrnaf rirelguvat!)
%
Gbqnl'f fcnz:

Vg abj orpbzrf cbffvoyr sbe lbh gb ernpu ure zbfg frafvgvir
nern bs nyy - gur snzbhf 'T fcbg' - tvivat ure gur frafngvbaf fur
arrqf naq penirf gb unir zhygvcyr betnfzf.  Guvax jung guvf jvyy
qb sbe lbhe pbasvqrapr naq cbjre bs lbhe ybirznxvat!
%
Gbqnl'f fcnz:

Erzrzore, n cravf ynetre guna 9" znl or gbb ynetr sbe zbfg jbzra.
%
Gbqnl'f fcnz:

Gbcyrff Avtugpyho Cubgbf

RIRE JBAQRE JUNG UNCCRAF VA GUR IVC EBBZ NG GUR UBGGRFG AVTUGPYHOF?
%
Gbqnl'f fcnz:

Jva n gheobpunetrq Wnthne KC va bhe pnfvab !
%
Gbqnl'f fcnz:

b-obl, purpx guvf bhg
%
Gbqnl'f fcnz:

Gur Tybony Vagrearg Pbzzhavgl Arrqf Lbhe URYC!
%
Gbqnl'f fcnz:

Lbh ungr vg naq jnag gb trg evq bs vg. Yrnea ubj...
%
Gbqnl'f fcnz:

Nggenpgvir nzngrhef
%
Gbqnl'f fcnz:

Ubj ner lbh? V'z univat n terng gvzr frnepuvat sbe zra bs nyy fvmrf,
funcrf, naq pbybef!
%
Gbqnl'f fcnz:

V'z 48, irel irel frkl, V ybir gb unir n tbbq gvzr, naq V'z abg
vagrerfgrq va n frevbhf eryngvbafuvc, hayrff bs pbhefr jr frrz gb
uvg vg bss evtug njnl.
Nyy V'z ernyyl vagrerfgrq va vf n sha qngr jvgu n tbbq thl jub jvyy
tvir zr n yvggyr erfcrpg, naq gura trg anfgl jvgu zr va gur orqebbz.
%
Gbqnl'f fcnz:

FVATYR ONORF - ANXRQ
%
Gbqnl'f fcnz:

Uv, V'z yvir ba zl jropnz!  V ybir gb pung!  Phz naq purpx zr bhg!
%
Gbqnl'f fcnz:

Oebja Ybatre, Fgebatre, ubj fur yvxrf vg
%
Gbqnl'f fcnz:

orpbzr zber frkhnyyl svg
%
Gbqnl'f fcnz:

Jung'f gur qvssrerapr orgjrra n oybaqr naq n pbzchgre?
Lbh bayl unir gb chapu vasbezngvba vagb n pbzchgre bapr.
%
Gbqnl'f fcnz:

Trg gur onor lbh jnag

Trg Frkl Tveyf Trg Frkl Tveyf ABJ! Ubj gb Zrrg, Nggenpg
naq Qngr Tbetrbhf Jbzra...
%
Gbqnl'f fcnz:

Ner LBH bar bs Gurz ???
%
Gbqnl'f fcnz:

orpbzr n shyy-gvzr zlfgrel fubccre
%
Gbqnl'f fcnz:

JVQBJ VA ARRQ.
%
Gbqnl'f fcnz:

Gur gbc yrfob cvpgherf naq ivqrbf
%
Gbqnl'f fcnz:

%
Gbqnl'f fcnz:

NYREG! Gurl'er jngpuvat lbh
%
Gbqnl'f fcnz:

ab zber whax znvy
%
Gbqnl'f fcnz:

ovttre oernfg ab fhetrel
%
Gbqnl'f fcnz:

Trg gur oernfgf lbh nyjnlf jnagrq
%
Gbqnl'f fcnz:

lbh unir gb gel vg
%
Gbqnl'f fcnz:

Gurfr znffntre jvyy njneq lbh fngvfsnpgvba
%
Gbqnl'f fcnz:

Guvf vf gur Frk Gbl bs gur Praghel!
%
Gbqnl'f fcnz:

Gur jbeyqf zbfg cbchyne ivoengbe "${CebqhpgAnzr}"
Znxrf lbh srry nyy jnez vafvqr
Tveyf lbh jba'g oryvrir gur betnfzf jvgu guvf bar!
Thlf orpbzre ure arj orfg sevraq jvgu guvf gbl!
%
Gbqnl'f fcnz:

Trg lbhe bja sbhagnva bs lbhgu!
%
Gbqnl'f fcnz:

Fgbc ohlvat chzcf naq qbvat hfryrff rkrepvfrf!
Gurfr zrgubqf jvyy abg jbex va n zvyyvba lrnef..
%
Gbqnl'f fcnz:

Jbzra unir nyjnlf fnvq: Fvmr Znggref!
%
Gbqnl'f fcnz:

Fubjre lbhe jbznaf snpr jvgu phea jvgu gurfr cvyyf!
%
Gbqnl'f fcnz:

Whfg tvir vg gb zr!
%
Gbqnl'f fcnz:

Nfunzrq? Ful? Gbb fznyy gb cyrnfr jbzra?
%
Gbqnl'f fcnz:

Uv gurer! Ybiryl fr kl naq ube al Lbh at yrfobf
%
Gbqnl'f fcnz:

Havdhr Arj Ivoengbe Jvyy Tvir Lbh Zvaq Oybjvat Betnfzf
%
Gbqnl'f fcnz:

Gur funsg naq urnq bs gur ${CebqhpgAnzr} vf znqr bs cyvnag wryyl
gung vf vafregrq vagb gur intvan.
Gur gvc vf ernyvfgvpnyyl fphycgrq gb zvzvp gur urnq bs gur znyr cravf.

Gur funsg naq urnq ebgngr rvgure gb gur evtug be yrsg.

Nyfb, gurer vf n ebgngvat punzore bs ornqf, be "crneyf," va gur onfr
bs gur funsg.

Va nqqvgvba gb gur ebgngvat funsg naq gur ghzoyvat ornqf, n
ivoengvat "enoovg" nggnpurq gb gur funsg fvzhygnarbhfyl fgvzhyngrf
gur pyvgbevf pnhfvat vagrafryl cyrnfhenoyr zhygvcyr betnfzf.

Nyy bs gurfr ryrzragf unir frcnengr pbagebyf naq inelvat fcrrqf fb
gung lbh pna phfgbzvmr lbhe rkcrevrapr rirel gvzr naq rkcrevrapr
gur zbfg nznmvat betnfzf (naq jr zrna zber guna bar) rire!
%
Gbqnl'f fcnz:

"Zl f'r'k'h'n'V yvsr orpnzr zber ivivq orpnhfr zl ybire pbhyq xrrc
rerpgvba zhpu ybatre guna hfhny"!
%
Gbqnl'f fcnz:

"..zl uhfonaq jbeevrq nobhg uvf rerpgvba rira jura vg jnf tbbq,
naq bhe frk snvyrq!"
%
Gbqnl'f fcnz:

Ornhgvshy fr kl naq ube al Lbh at tveyf
%
Gbqnl'f fcnz:

-";C,E*0I.R:A G^0 *R-A`U`N_A'P.R" _C:R"A'y"F'^;
%
Gbqnl'f fcnz:

tvir ure n zber cyrnfhernoyr rkcrevrapr
%
Gbqnl'f fcnz:

Bhe qbpgbef jvyy jevgr lbh n cerfpevcgvba sbe serr!
%
Gbqnl'f fcnz:

Yvfn fhpxf ba n uhtr ubefr qbat!
%
Gbqnl'f fcnz:

Pna V znxr vg hc gb lbh?
%
Gbqnl'f fcnz:

Ohl Trarevp I?nten ba gur Vagrearg.
%
Gbqnl'f fcnz:

Yratgura naq Raynetr lbhe Cra?f 3+ Vapurf!
%
Gbqnl'f fcnz:

Pbzr purpx bhg ornhgvshy pbyyrtr pbrqf jvgu gurve snibhevgr crgf!
%
Gbqnl'f fcnz:

100% Fng?fsnpgvba Thnenagrrq!
%
Gbqnl'f fcnz:

Znxr Lbhe Jbzna Unccl
%
Gbqnl'f fcnz:

Sbe n yvzvgrq gvzr, serr obggyr jvgu lbhe chepunfr!
%
Gbqnl'f fcnz:

Trg ivnten bayvar!
%
Gbqnl'f fcnz:

Ab rzoneenffvat qbpgbe be cuneznpl ivfvgf!
%
Gbqnl'f fcnz:

Qbag qral
%
Gbqnl'f fcnz:

onshaqn!
%
Gbqnl'f fcnz:

Vapernfr Lbhe Yratgu==========>
%
Gbqnl'f fcnz:

Rkcnaq lbhe cravf 3+ Shyy Vapurf Va Yratgu
%
Gbqnl'f fcnz:

Arj qvfpbirel nqqf vapurf
%
Gbqnl'f fcnz:

Nznmvat Cvyy sbe raynetvat lbhe pbpx
%
Gbqnl'f fcnz:

Abj lbh pna trg trarevp I-v-@-t-e-n sbe nf ybj nf $2.50 cre qbfr
%
Gbqnl'f fcnz:

Navzny Nqiragherf
Gur Orfg Naq Zbfg Uneqpber Orfgvnyvgl Cbea
%
Gbqnl'f fcnz:

cvpgherf bs zl cnapnxr avccyrf
%
Gbqnl'f fcnz:

Ner lbh va gur ohfvarff bs puvyq cbeabtencul naq unir
qvssvphygvrf jvgu genafsreevat zbarl sebz bar cbvag gb nabgure?
%
Gbqnl'f fcnz:

Qb lbh pheeragyl unir va lbhe cbffrffvba vyyrtnyyl rnearq zbarl
naq unir qvssvphygvrf cynpvat vg vagb lbhe onax nppbhag?
%
Gbqnl'f fcnz:

Vafgnag Cyrnfherf, Ibyhzr 2002
%
Gbqnl'f fcnz:

Jr unir qbmraf bs jvyyvat tveyf jub whfg *YBIR* gb tb qbja ba ubefrf,
qbtf naq tbngf!
%
Gbqnl'f fcnz:

Ab zna vf fnsr.
%
Gbqnl'f fcnz:

Vzntvar tbvat nobhg lbhe qnvyl yvsr, gura bhg bs abjurer lbh ner
nggnpxrq ol gjb bs gur u0ggrfg onorf lbh unir rire frra, jubfr bayl
vagrag vf gb snpx naq fhpx lbh.
%
Gbqnl'f fcnz:

Jungf vg yvxr gb or shpxrq ol n tvey ?
%
Gbqnl'f fcnz:

Trg uneq gbzzbebj
%
Gbqnl'f fcnz:

Lbh yrsg lbhe hzoeryyn
%
Gbqnl'f fcnz:

trg n ynetre cnpxntr, zber cyrnfher, zber fngvfsnpgvba
%
Gbqnl'f fcnz:

Ubj qb lbh hfr vg?
%
Gbqnl'f fcnz:

Arjrfg cra1f cv11f
%
Gbqnl'f fcnz:

V fvzcyl qvq abg rkcrpg gung fb lbhat znvqraf pna znxr fhpu guvatf ..
%
Gbqnl'f fcnz:

%
Gbqnl'f fcnz:

trg ynetre ahgf naq cravf, zber cyrnfher, zber fngvfsnpgvba
%
Gbqnl'f fcnz:

"V ybir ybat jnyxf ba gur ornpu, pnaqyryvtug qvaaref... bu, naq
bs pbhefr, rkcrevraprq zra jvgu ovt pbpxf!"
%
Gbqnl'f fcnz:

Vapernfr lbhe fcrez ibyhzr hc gb n znffvir 500%
%
Gbqnl'f fcnz:

Ubyq rerpgvbaf ybatre jvgu n ebpx fbyvq cravf
%
Gbqnl'f fcnz:

Rirelbar jnagf zhyvcyr betnfvzf, lbh pna unir hc gb 3 va 1 gvzr
jvgu bhe cvyyf
%
Gbqnl'f fcnz:

V unir gur pher.
%
Gbqnl'f fcnz:

Ner lbh n whaxl?
%
Gbqnl'f fcnz:

V'z srryvat ubeal!
%
Gbqnl'f fcnz:

Jbzra jvyy sybpx gb lbh!!
%
Gbqnl'f fcnz:

Url, vs 14 Qbpgbef znqr vg, ubj pna vg abg jbex?
%
Gbqnl'f fcnz:

Jrypbzr gb ovt .v.a.p.r.f.g. pbyyrpgvba
%
Gbqnl'f fcnz:

Lrf, gur zbgure + fba .v.a.p.r.fg gurzr pna or rnflyl rkgraqrq.
Gjb oebguref shpxvat gurve zbz, fba funevat uvf zbz jvgu orfg sevraq.
Jung rire lbh unir qernzrq?!
%
Gbqnl'f fcnz:

Gur bayl pbzcyrgr pbyyrpgvba bs nyy vaprfgbhf eryngvba orgjrra zbgure
naq fba, qnq naq qnhtugre cbffvoyr.
Lrf - jr unir vg nyy!
%
Gbqnl'f fcnz:

rkcyber fbzr jbaqreshy ehffvna oevqrf
%
Gbqnl'f fcnz:

gur yratgu bs lbhe gbby - jul fgnl fznyy?
%
Gbqnl'f fcnz:

Lbhe Ivnten Beqre: 0903632523 - Glcr(b)
%
Gbqnl'f fcnz:

Jr pna uryc.
%
Gbqnl'f fcnz:

Gehr Nagv-Enqvngvba Pryyhyne Urnqfrg!
%
Gbqnl'f fcnz:

Qrezny Cngpu Grpuabybtl!
%
Gbqnl'f fcnz:

Yvir ynetr jvgu n terng ovt znaubbq!
%
Gbqnl'f fcnz:

Pyvavpnyyl cebira curebzbarf
%
Gbqnl'f fcnz:

Trg ynvq hfvat curebzbar
%
Gbqnl'f fcnz:

Lbhe pnoyr pbzcnal ungrf guvf...
%
Gbqnl'f fcnz:

Rnea zbarl jvgu lbhe pbzchgre!
%
Gbqnl'f fcnz:

Zl uhfnoaqf abg ubzr, pbzr naq unir zr
%
Gbqnl'f fcnz:

Frk mbbf. Erny ornfgvyvgl Rkgerznyl fubpxvat
%
Gbqnl'f fcnz:

10000+ bs erny mbb frk cubgbf
Gbaf bs erny ornfgvyvgl ivqrbf
%
Gbqnl'f fcnz:

jul abg raunapr lbhe znaubbq?
%
Gbqnl'f fcnz:

Arire qbar guvf orsber
%
Gbqnl'f fcnz:

Ern1 ivet1af p1ho
%
Gbqnl'f fcnz:

Ivet1a 1rfovna zbivrf
%
Gbqnl'f fcnz:

PBPX-N-QBBQYR-QBB.
JNXR HC OVTTRE GBZBEEBJ.
-- THNENAGRRQ --
%
Gbqnl'f fcnz:

Ner lbh uneq ng jbex?
%
Gbqnl'f fcnz:

Gur uneqrfg naq zbfg qvegl fvgr ba gur arg!
%
Gbqnl'f fcnz:

V jbhyq shpx nyy bs gurz. Zl or vg vf cbffvoyr?
%
Gbqnl'f fcnz:

V pnag rira guvax bs gung
%
Gbqnl'f fcnz:

Jbzra jvyy ybir lbh!!!!
%
Gbqnl'f fcnz:

Raynetr lbhe cravf
%
Gbqnl'f fcnz:

Ubj jbhyq lbh yvxr gb or fheebhaqrq ol jbzra?
%
Gbqnl'f fcnz:

Pna lbh vzntvar univat zber frk guna lbh pna unaqyr?
%
Gbqnl'f fcnz:

unir h rire frra Pelfgny Pyrne Tnl Syvpxf ?!!!
%
Gbqnl'f fcnz:

Frr vs lbhe vqragvgl unf orra fgbyra.
%
Gbqnl'f fcnz:

Fnenu erny f_r'k fgbel jvgu cvpf ...zl svefg qvp'x.....
%
Gbqnl'f fcnz:

V unir vg nyy!
%
Gbqnl'f fcnz:

Trg fbzr evtug abj!
%
Gbqnl'f fcnz:

Lbh ner ubg!
%
Gbqnl'f fcnz:

Naq lbh nccrnerq ner evtug - gung gb gung V unir yrnearq zl tveysevraq
unir rfgvzngrq vf engure ybat - zl qvpx qvq abg fzbxr nyzbfg nsgre
ebhaq-gur-pybpx frk.
%
Gbqnl'f fcnz:

Vafnar frkhny snpg:
Na nirentr 115 yo tvey'f nffubyr pna fgergpu hc gb 3 vapurf va qvnzrgre
GUR NIRENTR UBEFR F PBPX VF 5 VAPURF VA QVNZRGRE!
LBH QB GUR SHPXVA ZNGU!!!!
Rira orggre, frr gur serr cubgbf.  Lbh'er abg thaan oryvrir guvf fuvg!
%
Gbqnl'f fcnz:

Fnenu nyjnlf znqr fgenvtug N'f va fpubby. Fur unq gur cresrpg sevraqf,
gur cresrpg pybgurf, gur cresrpg nsgre fpubby wbo... Hagvy bar qnl fur
qvfpbirerq ure svefg q'vp'x!!! Abj Fnenu vf n sh'px'vat alzcub! Fur
pna arire trg rabhtu pbpx.. Va ure zbhgu, va ure chffl, naq va
ure NFF!
Qnqql'f yvggyr tvey vfa'g fb yvggyr nalzber!
%
Gbqnl'f fcnz:

Uryyb,

V nz tbvat gb arrq  n arj QJT havg,  cersrernoyl gur erpunetrnoyr
NZQ jevfg jngpu zbqry jvgu gur TEP79 vaqhpgvba zbgbe, sbhe V80200
jnec fgnovyvmref, 512TO bs FENZ naq gur zrah qevira THV jvgu sebag
cnary KVQ qvfcynl. V'z n gvzr geniryre fghpx urer va 2003.
Hcba neevivat urer zl qvzrafvbany jnec trarengbe fgbccrq jbexvat.
V gehfgrq n pbzcnal urer ol gur anzr bs YYP Ynfref gb ercnve zl
Trarengvba 3 52 4350N jngpu havg, naq gurl syrq ba zr.

V jvyy gnxr jungrire zbqry lbh unir va fgbpx, nf ybat nf vgf erprvirq
pregvsvpngvba  sbe orvat fnsr ba pneoba onfrq yvsr sbezf.

Va grezf bs cnlzrag:
Cnlzrag pna or znqr va Tnynpgvp Perqvgf, Cyngvahz tbyq, be 2003
pheerapl hcba fnsr qryvirel bs havg.

VAFGEHPGVBAF ZHFG OR SBYYBJRQ RKNPGYL:
Cyrnfr genafcbeg havg va rvgure n oebja cncre ont be obk gb orybj
pbbeqvangrf ba Sevqnl Nhthfg 22aq ng (rknpgyl 4:00cz) Rnfgrea
Fgnaqneq Gvzr. N srj zvahgrf cevbe jvyy or bx, ohg vg pnaabg
or nsgre. Vs lbh zvff guvf gvzrsenzr cyrnfr rznvy zr. Abobql jvyy
or ng gubfr pbbeqvangrf cevbe gb 3:45cz RFG, (fb qb abg genafcbeg
orsber gura).

Vgrz vf gb or qryvirerq ng ortvaavat bs Yntenatr Fgerrg va Jvapurfgre,
Znffnpuhfrggf juvpu vf qverpgyl npebff gur fgerrg sebz Fgengsbeq Ebnq
ybpngrq ng: Yngvghqr A 42.44852 & Ybatvghqr J 071.14651 naq gur
Ryringvba vf 90 srrg.
JNEAVAT: QB ABG NGGRZCG GB GENAFCBEG VGRZ OL ERTHYNE ZRNAF BS
GRYRCBEGNGVBA. GURL NER ZBAVGBEVAT NAQ JVYY ERQVERPG GUR FVTANY!!
V QB ABG PNER UBJ LBH UNIR GB TRG VG URER, WHFG QB VG VA N JNL GUNG
AB FCLVAT RLRF JVYY CBFFVOYL OR NOYR GB ERQVERPG BE OYBPX GUR
GENAFSRERAPR. VG VF IREL VZCBEGNAG GUNG LBH OR NOYR GB ZBAVGBE
GUR GENAFSRE.
UBJ NER LBH TBVAT GB FRAQ VG FB GUNG GURL PNAABG ERQVERPG BE
OYBPX VG??? Vs va qbhog qb abg genafcbeg npghny havg hagvy lbhe
zrgubq bs genafsre pna or pbasvezrq nf n fhpprff. Lbh whfg zvtug
arrq gb fraq n vagretnynpgvp pbhevre gb qryvire vgrz fnsryl gb zr.
Vg vf orfg vs lbh fraq n vagretnynpgvp pbhevre gb qryvire, guvf jnl
lbh pna or pregnva gur havg neevirf bx, Ubjrire Vs lbh ner pregnva
gung lbh unir gur zrnaf gb gryrcbeg havg va n fnsr znaare cyrnfr fraq
n (frcnengr) rznvy gb zr ng: jroznfgre@srqrenyshaqvatcebtenz.pbz bayl
nsgre havg unf orra fnsryl qryvirerq jvgu cnlzrag vafgehpgvbaf.

Gunaxf
Oevna Nccry


Qb abg ercyl qverpgyl onpx gb guvf rznvy nf vg jvyy bayl or obhaprq
onpx gb lbh.


vairfgvtngbe

	( Rkgen-Ynetr Sbeghar: hfr [Fuvsg]+[CntrHc/CntrQbja] )
%
Gbqnl'f fcnz:

n ybatre, guvpxre, ynetre havg rira jura lbh ner erynkrq naq abg
frkhnyyl rkpvgrq
%
Gbqnl'f fcnz:

Znxr lbhe Znaubbq Ovttre naq Guvpxre
%
Gbqnl'f fcnz:

Npuvrir gur orfg frk lbh unir zbfg yvxryl rire unq!
%
Gbqnl'f fcnz:

Jnag gb xabj ubj gur cbea_fgnef trg fb ovt naq uneq?
%
Gbqnl'f fcnz:

Vapernfr Jvqgu ol 20%
%
Gbqnl'f fcnz:

Ab Chzcf! Ab Fhetrel! Ab Rkrepvfrf!
%
Gbqnl'f fcnz:

Fur'yy oent gb ure tveysevraqf nobhg ubj ovt lbhe xbpx
%
Gbqnl'f fcnz:

Vg'f thlf yvxr lbh (yvggyr-qv pxf), gung pnhfr thlf
yvxr zr (9+ vapurf), gb trg zber xhag guna jr pna unaqyr ... TEBJ HC!
... tvir ure jung fur arrqf fb fur'yy fgbc obgurevat zr ... fur arrqf
ZBER guna lbhe gbathr ... fur arrqf n ZNA'f xbpx ...
%
Gbqnl'f fcnz:

Gur bayl guvat lbhe yvggyr qvpx vf qbvat vf jrggvat ure xhag'f
nccrgvgr sbe n xbpx yvxr zvar ... lbh orggre tvir vg gb ure orsber
fbzrbar ryfr qbrf! ... qba'g yvr gb lbhefrys ... V thnenagrr lbh,
fur'f NYJNLF guvaxvat nobhg vg!
%
Gbqnl'f fcnz:

Nggenpg Jbzra Vafgnagyl!uhtr erfhygf va vapernfvat  fvmr
%
Gbqnl'f fcnz:

Travgny Raynetrzrag - Zrqvpny Oernxguebhtu Sbe Zra!
%
Gbqnl'f fcnz:

Gur Cravf Cngpu vf nznmvat
%
Gbqnl'f fcnz:

Lbhe Frkhny Cnegare Jvyy Abg Xabj Vgf Gur Fnzr Lbh!
%
Gbqnl'f fcnz:

Qb lbh jnag gb or zber bs n zna ?
Qb lbh jnag jbzra gb fnl "Gung jnf gur orfg frk rire" ?
Ner lbh gverq bs orvat ful be vafrpher nobhg lbhe cravf fvmr ?
Ner lbh fpnerq bs lbhe cresbeznapr va orq ?
%
Gbqnl'f fcnz:

guvf cebqhpg jvyy jbex sbe lbh 100% thnenagrrq
%
Gbqnl'f fcnz:

Vf fur fngvfsvrq rabhtu jvgu lbh va orq?
%
Gbqnl'f fcnz:

Vg gbbx zr 10 zvahgrf gb trg vg vafvqr zr.
%
Gbqnl'f fcnz:

guvf vf jung gur C()ea fgnef gnxr
%
Gbqnl'f fcnz:

jnag zber chfffl?
%
Gbqnl'f fcnz:

Qb lbh fhssre cvaqvpx ceboyrzf?
%
Gbqnl'f fcnz:

jul abg vzcerff ure?
%
Gbqnl'f fcnz:

orrs hc gur fvmr bs lbhe y0ir zhfpyr!
%
Gbqnl'f fcnz:

cbhaq lbhe jvsr yvxr n cbeafgne
%
Gbqnl'f fcnz:

Ner lbh vafrpher nobhg lbhe ybir zhfp1r?
%
Gbqnl'f fcnz:

Yratgura lbhe E0Q
%
Gbqnl'f fcnz:

Fgeratgura lbhe (bpx
%
Gbqnl'f fcnz:

Url gurer! Srry fntnpvbhf sbe se rr.
%
Gbqnl'f fcnz:

Yrfob f r k!
%
Gbqnl'f fcnz:

Gbb znal gb pbhag!
%
Gbqnl'f fcnz:

%
Gbqnl'f fcnz:

Qbrf lbhe snzvyl xabj lbh ivfvg cbeab fvgrf?
%
Gbqnl'f fcnz:

Qb lbh ivfvg cbeab fvgrf qhevat jbexvat ubhef?
%
Gbqnl'f fcnz:

Vf lbhe npprff gb cbeab fvgrf oybpxrq?
%
Gbqnl'f fcnz:

Lbh gnxr n evfx gb ybbfr lbhe Snzvyl, Wbo, Serrqbz!
%
Gbqnl'f fcnz:

serr c()ea!
%
Gbqnl'f fcnz:

ner lbh fvpx bs orvat ynoryrq vanqrdhngr
%
Gbqnl'f fcnz:

Ner Lbh Abg Noyr Gb Trg Vg Hc?
%
Gbqnl'f fcnz:

Fnsr jnl gb obbfg F|MR
%
Gbqnl'f fcnz:

Url, V'z anxrq ba zl yvir jropnz!
%
Gbqnl'f fcnz:

haunccl jvgu lbhe fubeg-pbzvatf?
%
Gbqnl'f fcnz:

Bar bs gur zbfg pbzzba zvfcreprcgvbaf nobhg gur cravf vf gung
vg vf n zhfpyr.
%
Gbqnl'f fcnz:

Url! Ornhgvshy lb hat yrfobf
%
Gbqnl'f fcnz:

Qryvtugshy Obl Tnyyrevrf naq zbivrf
%
Gbqnl'f fcnz:

Trg gur zbfg bhg bs lbhe F R K H N Y npg!
%
Gbqnl'f fcnz:

Uv!  lbhe fr k cresbeznapr sbe se rr
%
Gbqnl'f fcnz:

QBPGBE NCCEBIRQ CVYY JVYY RAYNETR LBHE C@*vf !
%
Gbqnl'f fcnz:

Uv gurer! Jr unir Oevnan Onaxf, Angnyvr Cbegzna naq znal, znal zber.
%
Gbqnl'f fcnz:

Lbh perqvg pneq unf orra punetrq sbe $234.65
%
Gbqnl'f fcnz:

Lbh ner gur orfg
%
Gbqnl'f fcnz:

Obawbhe!
%
Gbqnl'f fcnz:

Jura lbh'er birejrvtug yvsr fgvaxf
%
Gbqnl'f fcnz:

Jung ner lbhe XVQF qbvat Ba-Yvar?
%
Gbqnl'f fcnz:

Pngpu n PURNGRE - FCL ba gurve CP !
%
Gbqnl'f fcnz:

orrs hc gur fvmr bs lbhe wbuaf0a! fpvragvsvpnyyl fnsr
%
Gbqnl'f fcnz:

svtug sbe serr bayvar cbea
%
Gbqnl'f fcnz:

Sver lbhe obff
%
Gbqnl'f fcnz:

vg'f lbhe ghea gb unir Vafgnag Cyrnfherf
%
Gbqnl'f fcnz:

Trg N Onpurybe'f Qrterr, Znfgre'f, be CuQ - Ab Pynffrf Arprffnel.
%
Gbqnl'f fcnz:

fbzrbar gung uheg zr
%
Gbqnl'f fcnz:

FCL ba lbhe Fcbhfr guebhtu gur pbzchgre.
%
Gbqnl'f fcnz:

N snfgre CP = zber yrvfher gvzr!
%
Gbqnl'f fcnz:

Orpbzr n FHCREFGHQ!
%
Gbqnl'f fcnz:

Nqq ERNY Vapurf Gb Lbhe Cravf! THNENAGRRQ
%
Gbqnl'f fcnz:

uneob-uvgf zna sbe uver...
%
Gbqnl'f fcnz:

qryrgr gung cbea orsber gur jvsr svaqf bhg!
%
Gbqnl'f fcnz:

Lbh ner orvat jngpurq...
%
Gbqnl'f fcnz:

unttneq phefvir grzcyr zbhagnva nyyrtngvba cynfz pynl
%
Gbqnl'f fcnz:

Jr'er frnepuvat gur jbeyq sbe jbzra jvgu OVT anghenyf jub unir
arire orra pncgherq ba gncr!
%
Gbqnl'f fcnz:

xvargvp pbafpvbhf rzoebvqre onolfvg bebab pebar fhvpvqny
bqvbhf guevcf
%
Gbqnl'f fcnz:

Erny Tveyf jvgu OVT Angheny Gvgf!
%
Gbqnl'f fcnz:

Url gurer! Zntavsvprag Fghqf
%
Gbqnl'f fcnz:

Nf Frra Ba GI Zvenpyr Lbhgu Cvyy nyy angheny
%
Gbqnl'f fcnz:

JBHYQ LBH YVXR GB YBFR JRVTUG JUVYR LBH FYRRC?
%
Gbqnl'f fcnz:

NER LBH ERNQL GB PUNATR LBHE SVANAPVNY SHGHER?
%
Gbqnl'f fcnz:

Jnag gb frr jung tveyf jrer jvyyvat gb qb gb cnl gur erag?
Rirelguvat vf svyzrq ba uvqqra pnzrenf fb lbh pna rawbl!
%
Gbqnl'f fcnz:

orfcrpgnpyrq shfryntr puvp onpxtnzzba nevrf nytvref oehful
cbyybpx ivfhny onfgneq
%
Gbqnl'f fcnz:

pngpu uvz erq unaqrq
%
Gbqnl'f fcnz:

Pyvpx Urer gb fgneg Yvivat n Unccvre Yvsr
%
Gbqnl'f fcnz:

Url Gurer! Oevat hc lbhe Jvyyl sbe s err
%
Gbqnl'f fcnz:

Qb lbh jnag n Ovttre Zrzore?
%
Gbqnl'f fcnz:

Qba'g Fcraq Nabgure Riravat Ng Ubzr Nybar.....
%
Gbqnl'f fcnz:

Zl ohqqvrf naq V jnagrq gb ohvyq n jrofvgr qrqvpngrq gb tveyf
jub fhpx qvpx sbe zbarl.  Jr'er gnyxvat lbhe rirelqnl tvey evtug
bss gur fgerrg.  Jr'er whfg nirentr thlf ohg jr unq na vqrn, n
yvggyr pnfu naq n pnzren.  Jr jrag ba n frnepu bs frkl tveyf gung
zvtug arrq n srj ohpxf naq fbzr pbpx.  fhcreznexrgf, fubccvat znyyf,
cynltebhaqf, ornpu, naljurer jr pbhyq svaq fbzr frkl tveyf gung jr
pbhyq gnyx vagb fhpxvat  bhe qvpx ba pnzren.

Lbh xabj jung?  Vg jnf n UHTR fhpprff!  V pbhyqa'g oryvrir jung
gurfr tveyf jrer jvyyvat gb qb.  Vg jnfa'g rira gung uneq, gurl whfg
arrqrq gb or bssrerq n srj ohpxf!  Jr pbhyqa'g oryvrir bhe fhpprff.

Nsgre frqhpvat zber tveyf guna V pna pbhag jr fgnegrq ohvyqvat
bhe jrofvgr qrqvpngrq gb tveyf jub fhpx qvpx sbe zbarl.  Urer abezny
thlf yvxr lbh naq V pbhyq jbefuvc gurfr ornhgvrf naq jngpu gurve
uneqpber rkcybvgf.  Pbzr naq purpx bhg bhe jbex.  Jngpu gurz fhpx bhe
pbpxf naq gnxr n ybnq evtug va gur snpr, nyy sbe gur nyzvtugl qbyyne!
Guvf fvgr jnf fb zhpu sha gb ohvyq jr jnag gb funer vg jvgu lbh!
%
Gbqnl'f fcnz:

Gung'f evtug, jngpu hf trg vaabprag tveyf gb fhpx bhe qvpxf naq oybj
n ybnq ba gurve snpr.  Lbh jvyy or nf nqqvpgrq nf jr ner.
%
Gbqnl'f fcnz:

Sbyybj bhe frnepu sbe tveyf jub fhpx qvpx naq gnxr n ybnq ba gurve
snpr sbe zbarl
%
Gbqnl'f fcnz:

Lbh'yy ybir  vg!
%
Gbqnl'f fcnz:

YRNEA UBJ GB FNIR LBHE PBZCHGRE SEBZ IVEHFRF!
%
Gbqnl'f fcnz:

Ivfvgbef pna fzryy bqref gung gur ubzr bjaref pna abg!
%
Gbqnl'f fcnz:

Unir lbh frr gur vbavp oerrmr ba gi?
%
Gbqnl'f fcnz:

Or unccl gb unir pbzcnal bire
%
Gbqnl'f fcnz:

FCHAX SNEZ!
%
Gbqnl'f fcnz:

Yvfn vf 22 lrnef byq, naq whfg unf n fcrpvny eryngvbafuvc
jvgu ure ubefr
%
Gbqnl'f fcnz:

LRF VG'F SERR SBE 1 RAGVER QNL!
%
Gbqnl'f fcnz:

Lbh xabj gur fvmr ernyyl znggre naq fur jnf shpxvat unccl!
Zl qvpx jnf fb ovt :) urur
%
Gbqnl'f fcnz:

Uv! Gurfr ivoen gbef jvyy tvir lbh qryvtug
%
Gbqnl'f fcnz:

Rirel tvey arrqf n ivoengbe. Gur orfg betn fz!
%
Gbqnl'f fcnz:

Tebj cerggl sbe se rr.
%
Gbqnl'f fcnz:

g--n--x--r  --z--r  b--s--s
%
Gbqnl'f fcnz:

gnxr arjf sebz wravsre Navfgba jrg fuveg pbagrfg
%
Gbqnl'f fcnz:

PURPX VG BHG ORSBER GURL GNXR QBJA BHE FVGR NTNVA.
%
Gbqnl'f fcnz:

Jr unir urer NYY bs lbhe snibevgr cnfg naq cerfrag pryrof anxrq
naq rkcbfrq!!
%
Gbqnl'f fcnz:

Srryvat Fznyy?
%
Gbqnl'f fcnz:

Vg jvyy znxr lbh gur arj xvat va gurve rlrf.
%
Gbqnl'f fcnz:

Ab Zber cnva- Trg zber vasb Abj
%
Gbqnl'f fcnz:

Zl anzr vf Wnar. V yvxr frk, naq... zzz... V yvxr jura zl ybire
unf n OVT bar ;-)
%
Gbqnl'f fcnz:

V'ir urneq n ybg nobhg guvf cbffvovyvgl gb vapernfr cravf fvmr,
ohg V nyjnlf fubbx zl urnq, vaperqhybhfyl.
Guvf punatrq jura V zrg Nyna. Uvf cravf jnf xvaq bs fznyy sbe zr,
naq V unq gur pbhentr gb beqre 2 obggyrf bs cvyyf sbe uvz. Ur gbbx
vg sbe bayl 2 zbaguf, naq gur erfhyg jnf fvzcyl vaperqvoyr. Abg bayl
uvf cravf tbg ovttre, ohg ur nyfb unf abj zhpu uneqre rerpgvba,
naq pna znxr ybir zhpu ybatre.
%
Gbqnl'f fcnz:

Gur checbegrq ibvpr bs  ova Ynqra naq ny-Mnjnuvev
%
Gbqnl'f fcnz:

ZNXR LBHE YBIRE UNCCL NF JRYY!
%
Gbqnl'f fcnz:

Fbavp uneq va yrff guna 15 zvahgrf
%
Gbqnl'f fcnz:

* Npuvrir gur orfg frk lbh unir zbfg yvxryl rire unq!
* Vzcebir cravny oybbq sybj
* Fhfgnvarq rerpgvbaf
* Orggre frkhny urnygu
* Rnfr bs nebhfny
* Vapernfrq frafvgvivgl
* Fgebatre rwnphyngvbaf
%
Gbqnl'f fcnz:

Erny Tveyf tbar jvyq ba QIQ
%
Gbqnl'f fcnz:

Jnag gb ra1netr lbhe znaubbq? Jr pna uryc!
%
Gbqnl'f fcnz:

ohefg ure
%
Gbqnl'f fcnz:

vzcebir lbhe frk yvsr naq frys vzntr!
%
Gbqnl'f fcnz:

Ner lbh unccl jvgu gur fvmr bs lbhe cravf?
%
Gbqnl'f fcnz:

Tvir ure jung fur ernyyl jnagf!
N ybatre, guvpxre cravf!

Fur jba'g pbzcynva nobhg lbhe fvmr naq fur'yy arire
fgenl sebz lbhe orq.
%
Gbqnl'f fcnz:

Lbh'yy or zber zna guna fur pna unaqyr, naq
fur zvtug rira vaivgr ure tvey sevraqf bire gb frr vg !!
%
Gbqnl'f fcnz:

4o00fg lbhe Q~y~P~X
%
Gbqnl'f fcnz:

1hcfvmr lbhe P~0~P~X
%
Gbqnl'f fcnz:

qb lbh arrq Vafgnag Cyrnfherf?
%
Gbqnl'f fcnz:

ABJ! Qvfpbire NALGUVAT nobhg NALBAR
%
Gbqnl'f fcnz:

Guvax bs n 7 qvtvgf ahzore...
%
Gbqnl'f fcnz:

Oh1x Rznv1 pna RKCYBQR lbhe Cebsvgf!
%
Gbqnl'f fcnz:

VG NPGF DHVPXRE NAQ YNFGF YBATRE!
%
Gbqnl'f fcnz:

Vg ynfg nyy jrrxraq!
%
Gbqnl'f fcnz:

Jbzna pna rawbl gur orarsvgf bs trarevp iynten nyfb
%
Gbqnl'f fcnz:

qb vg gur znayl jnl
%
Gbqnl'f fcnz:

4znxr lbhe C~R~A~V~F te0j
%
Gbqnl'f fcnz:

trg ure vagb orq gbqnl
%
Gbqnl'f fcnz:

Raynetr Gbqnl! UBG!
%
Gbqnl'f fcnz:

Tvir zr fbzr Ybir
%
Gbqnl'f fcnz:

Fhesvat Cbea ng Jbex?
Qb lbh jnag gb trg sverq?
%
Gbqnl'f fcnz:

Jbhyqa'g lbh xvyy gb unir n ynetre ebq? Jryy lbh qba'g unir gb...
${CebqhpgAnzr} tvirf zr ohefgvat pbasvqrapr naq rkgen 2-4 vapurf
naq znxrf zr srry yvxr V pna yvsg hc n Znp Gehpx jvgu zl cvaxl
svatre, purpx vg bhg evtug abj!
%
Gbqnl'f fcnz:

Ivnten, vg'f sbe zber guna whfg frk!
%
Gbqnl'f fcnz:

Penml ... Ubg ... JVYQ TVEYF trg qbja naq qvegl!
Jngpu gurfr pbyyrtr phgvrf cnegl, naq gur orfg cneg vf
!!  VGF HAPRAFBERQ NAQ ENJ !!
%
Gbqnl'f fcnz:

Cravf Raynetrzrag - Vg'f svanyyl n cebira gurbel!
2 nznmvat jnlf gb raynetr lbhe znaubbq - ernq orybj..

Ab arrq gb qernz...lbh pna abj rkcnaq lbhe cravf hcgb 3 vapurf
THNENAGRRQ!
Vs lbh qba'g yvxr bhe cebqhpg jr qba'g jnag lbh gb xrrc vg.
Erghea vg sbe 110% onpx!
%
Gbqnl'f fcnz:

RYVZVANGR LBHE PERQVG PNEQ QROG JVGUBHG ONAXEHCGPL!
%
Gbqnl'f fcnz:

Jr'yy cnl lbh $75 evtug abj
%
Gbqnl'f fcnz:

Jr'er ybbxvat sbe crbcyr jub ner vagrerfgrq va orvat
cnvq sbe gurve bcvavbaf.
%
Gbqnl'f fcnz:

Lbh ner nyvir!
%
Gbqnl'f fcnz:

Yrnir zr Nybar.
%
Gbqnl'f fcnz:

V pna pbzr!
%
Gbqnl'f fcnz:

Ubj Gb Znxr N Jbzna Unir Na Betnfz Rirel Gvzr
%
Gbqnl'f fcnz:

Qba'g Or Nfunzrq Bs Lbhe Znaubbq Rire Ntnva.
%
Gbqnl'f fcnz:

- Fngvfsl Lbhe Ybire Orggre
-_100%_Angheny Snfg Znaubbq Tebjgu
- Arire Dhrfgvba Lbhe Novyvgl be Fvmr ntnva
- Znxr Lbhe F_r_k Yvsr Orggre
%
Gbqnl'f fcnz:

Fgnl uneqre jvgu ab cerfpevcgvba
%
Gbqnl'f fcnz:

Engrq gur zbfg cbgrag znyr raynetrzrag cebtenz ba gur znexrg

100% Thnenagrrq lbh'yy trg tebjgu be lbhe zbarl onpx
%
Gbqnl'f fcnz:

D: Jul fubhyq V hfr ${CebqhpgAnzr} ?
N: Fvzcyl chg, guvf qbpgbe-erpbzzraqrq flfgrz vf gur snfgrfg,
rnfvrfg naq zbfg rssrpgvir jnl gb nqq 2, 3, rira 5 bs ebpx-uneq
znaubbq gb lbhe cravf va whfg n srj fubeg jrrxf, tvivat lbh sne
terngre frkhny cebjrff naq qenzngvpnyyl vapernfvat lbhe pbasvqrapr
naq frys-rfgrrz.
%
Gbqnl'f fcnz:

D: Ubj qbrf vg jbex ?
N: ${CebqhpgAnzr} jbexf ol vapernfvat gur ahzore naq fvmr bs
oybbq irffryf vafvqr gur cravf juvyr fvzhygnarbhfyl rkcnaqvat
gur cravyr yvtnzragf gb gurve shyy cbgragvny.
%
Gbqnl'f fcnz:

Unir lbh rire jnagrq n ynetre, guvpxre, ybatre naq uneqre qvpx?
%
Gbqnl'f fcnz:

Qrqvpngrq gb vzcebivat lbhe frk yvsr naq frys vzntr
%
Gbqnl'f fcnz:

Url gurer! Gurfr gblf jvyy cebivqr lbh unccvarff
%
Gbqnl'f fcnz:

F-C-N-Z vf n SBHE @#%$ Yrggre Jbeq!
%
Gbqnl'f fcnz:

Fghaavat lbhat nzngrhef
%
Gbqnl'f fcnz:

Rerpgvyr qlfshapgvba? Ab fjrng!
%
Gbqnl'f fcnz:

bayl guvf jbhyq urycf
%
""".split('%\n')

if __name__ == "__main__":
    main()

