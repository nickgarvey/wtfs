#!/usr/bin/env python3
#
# wtfs.py will mount a filesystem at a directory and produce some
#         files with spam messages inside
#
# Author: Nick Garvey
#
# The word list used to generate the filenames and the spam messages
# are included directly in this file

import codecs
import hashlib
import random
import stat
import sys
import time

from fuse import FUSE, Operations


DIR_ENTRY_RANGE = (8, 20)
REGEN_CONTENTS_TIMEOUT = 3 # seconds


def get_index(path):
    return path.__hash__() % len(SPAMS)


def get_spam(path):
    rot13 = codecs.getencoder('rot-13')
    index = get_index(path)
    # Fortune gives you the files in rot13 for some reason
    spam = rot13(SPAMS[index])[0]
    # First two lines are always "Today's Spam:" and a newline
    # so trim those and the final trailing newline
    spam_text = "\n".join(spam.split('\n')[2:])
    return spam_text


def get_word(seed):
    # Use hashlib here so the directory entries are more random
    md5 = hashlib.md5()
    md5.update(seed)
    hash_int = int.from_bytes(md5.digest(), byteorder='little')
    index = hash_int % len(WORDS)
    return WORDS[index]


class WTFS(Operations):
    def __init__(self, *args, **kwargs):
        self.__set_dir_contents()

    def __set_dir_contents(self):
        now = int(time.time())
        self.last_readdir_time = now
        self.dir_contents = (
            ['.', '..'] +
            [get_word((now + i).to_bytes(8, byteorder='little'))
             for i in range(random.randint(*DIR_ENTRY_RANGE))]
        )

    def readdir(self, path, offset):
        for dir_entry in self.dir_contents:
            now = int(time.time())
            if self.last_readdir_time < now - REGEN_CONTENTS_TIMEOUT:
                self.__set_dir_contents()
            self.last_readdir_time = now
            yield dir_entry

    def getattr(self, path, fh=None):
        attrs = {
            'st_atime': self.last_readdir_time,
            'st_ctime': self.last_readdir_time,
            'st_mtime': self.last_readdir_time,
        }
        if path == '/':
            attrs.update({
                'st_mode': stat.S_IFDIR | 0o555,
                'st_nlink': len(self.dir_contents),
            })
        else:
            attrs.update({
                'st_mode': stat.S_IFREG | 0o444,
                'st_nlink': 1,
                'st_ino': get_index(path),
                'st_size': len(get_spam(path)),
            })
        return attrs

    def open(self, path, flags):
        return 0

    def read(self, path, length, offset, fh=None):
        return get_spam(path)[offset:offset+length].encode('utf-8')


def main():
    if len(sys.argv) != 2:
        print("usage: {} mountpoint".format(sys.argv[0]))
        sys.exit(1)
    fuse = FUSE(WTFS(), sys.argv[1])


WORDS = """
abbreviation
abetted
abide
aboriginal
about
abrasive
abscond
absolves
absorbs
abundance
abuser
acceptability
acceptable
acclimatizing
accountancy
acid
acquittal
acrylics
ad
addressed
adjourned
adults
advance
adverb
affair
affect
affects
affirmation
affirmations
affirmative
affronting
agility
agony
aides
airier
albums
alcoves
alerts
aliased
alive
allowance
alloys
am
ameer
amendment
amphitheater
amusement
annoy
annoyingly
antagonistic
anthill
antibiotics
anxieties
apex
apologized
appallingly
appealing
append
applies
appraise
apprehended
apprenticeship
appropriations
arbitrating
archaeologist
archeological
arcing
ares
argue
armaments
armistice
arranges
articulate
artwork
ascensions
ashtray
asking
assails
assembled
assenting
assigning
assists
astrology
astronaut
astute
asylums
atmosphere
atmospheric
attains
attempted
attendants
attiring
attractions
attributes
auguster
authoring
authoritatively
authorizations
automation
autopsies
averse
avoids
awfully
awhile
awry
baboons
baking
ballooned
bandier
banding
bandstands
bani
banker
barbed
bare
bared
barely
barges
barrette
basis
bathed
beating
bedroom
beehives
beggar
beheading
belching
believable
bellboys
bellied
betrothals
bettors
bilateral
biographical
biped
bit
bitterer
bitterly
bitterness
blackberrying
blackbird
blackmailed
blanketing
bleeds
blesses
blew
blithely
blobbed
blogged
bloom
blotching
blousing
bluebirds
blueprints
bluntest
blurt
blushed
boastful
bodyguard
boil
boldest
bomb
bombard
bombed
bombs
bond
boning
bookcases
bookshelf
boomeranged
boor
bores
born
bouquet
boxcars
braced
bragged
bragging
brainstorming
brandies
brash
brashest
brass
brassiest
breakfast
breaking
breasts
brew
bringing
bristling
britches
brooches
browbeaten
brown
brutally
bubble
bucketing
buffed
builder
bull
bullion
bunk
bunkers
burbled
burden
burials
burns
burros
butchering
buzzes
cabinets
caffeine
cages
calibrates
call
callable
cancelation
candling
cannibals
cannons
canopies
cans
canvased
canvassed
capacitors
capitalist
capitalized
capitulates
captures
carbon
cardigan
caress
caressed
carriage
carrier
castes
cataloged
catapulted
catapulting
catastrophe
catcall
categorically
caulk
caulks
caution
cavalry
caverns
cavorted
celebrated
celibate
cement
censoring
ceremonious
chagrined
chains
chair
chameleon
chaperoned
charging
check
cheerfuller
cheerfullest
chemical
cherish
chestnuts
chilled
chime
chimes
chirping
chivalry
chocolates
cholera
choppier
chortles
chrome
chug
circulars
circumstance
circumvent
clammed
clamped
clasps
classification
classrooms
cleansers
clearing
clearings
cleavage
cleaved
click
clicks
clinical
clipping
close
clouded
cloudy
clue
clues
clumsier
cob
cobweb
cock
cockpit
cocks
cocktails
coincided
coincidentally
coke
coked
collarbone
collective
collie
collision
colonel
colonize
combinations
combustion
come
comets
comings
commanders
commences
commendable
commerce
commercial
commoner
communicable
communing
commuters
company
comply
compose
compounds
comprehended
compress
computers
con
concatenated
concatenating
concealing
concentrated
concludes
conclusion
conclusions
condensation
condiments
conditioned
conditioning
condone
cone
confections
confederation
confides
confined
confinement
confounding
conical
conjugation
connected
consecrates
consecutive
consequent
consignment
consists
consoled
conspirators
constructions
consult
consultants
consume
consumers
consummate
contaminate
contemplatives
contemporaries
contorting
contraceptives
contraction
contributor
convening
converters
convertor
conveyances
convulsions
cools
cooper
cornmeal
corporations
corrected
correspondent
corrupt
cosmonauts
cottonwood
councillors
counter
counteracted
counteracting
countersign
countries
courtyards
coves
covetous
cowed
coyer
crabs
crackpot
crafts
crank
crassest
craze
crazily
creeping
criminally
crimsons
crippled
crises
crispest
crisscrossing
crockery
crossbows
crossings
crouch
crowbar
crumbs
crystalizing
cued
cuisine
culmination
cultural
curries
cursory
curtsy
curves
curving
custard
customers
cymbals
dabbed
daintier
dandiest
darkness
dashing
dawned
daydreams
dealer
debility
debriefing
debug
decease
deceases
declarations
decorates
decree
deeding
defaced
defaming
defaulting
defiance
definite
deftly
deigned
deity
dejecting
deliberated
delicate
delirious
deltas
demagog
demean
demeanor
demerit
democrats
demonstrably
demonstratives
denouncing
denting
dentists
departmental
departs
deploring
derails
derange
desirous
despatching
despite
despots
destining
destroyers
deteriorated
determines
detonates
devastated
deviling
devils
devoted
devotee
diaphragms
dictatorship
differentiating
dig
digested
digital
diked
dilated
dimension
diminishing
dimly
diphthong
directs
dirge
disable
disables
disagreeing
disallow
disappears
disappoint
disapproved
disapproves
disbelieving
disburse
disclosure
discolors
discredit
discreetest
discriminate
disembarkation
disincentive
disinterested
disks
dislocations
disobeying
disordered
disorderly
dispersal
displaying
displeases
dissimilar
dissuaded
dissuading
distinctly
distinguishing
distract
distracts
disturbs
dittoes
diver
divining
division
documentation
dodging
does
doggedly
dogging
domed
domiciled
dominant
dons
doodled
dotted
doubtfully
downgrades
drains
drapery
drawings
dried
driest
drives
drowning
drugstores
drunk
duel
dully
dutiful
duvet
dynamited
eagle
earliest
earmarked
earnest
ecologists
ecstasy
eddies
effecting
effigies
elder
electors
electrodes
elicit
elicited
eliminating
eloped
email
embalm
embalmed
embargoes
embarks
embedding
embossed
embraces
embroider
embroideries
embryos
emigrants
emissary
emulator
emulsion
encircled
encoring
encryption
encumbrances
endangers
endeared
endlessly
enforce
engrave
enjoyment
enquire
enraged
entrap
enumerated
envies
environmental
epaulets
epics
epoch
epsilon
errand
erupt
essence
establishment
esteemed
estimate
ethical
evangelistic
evenly
eves
evil
eviler
eviller
exacting
exampling
excavating
excels
exchanged
exclusion
exemplifies
exhibition
exhumes
exists
exoduses
expanded
expectant
expeditions
experimenting
expertise
exposing
exterminate
extoll
extract
extremer
fabricating
fact
faeces
falter
fanatics
fanciest
farewell
fasten
fastenings
favorably
fears
federalism
feed
feels
felts
fenced
fend
ferocity
fertility
fibbing
fidelity
fiercest
fifties
filth
finally
finger
fins
fir
fireman
fireplaces
firework
firms
fish
fittest
fiver
fixing
fixture
flag
flagstone
flare
flared
flat
flawless
fledged
fledgling
fleeces
fleeing
flinches
flipper
flirtatious
flogs
floweriest
fluffed
flurried
flurry
folders
folks
fooling
footnote
footpaths
footprint
forewords
forgave
forking
forte
forwardest
fossilize
fouling
foundlings
fount
fountain
frailer
frailest
framed
franks
freckling
freeway
freighted
freighter
frenzied
frequenting
fright
fringe
frog
frostbiting
frothiest
frying
fudge
fulfilling
fulfilment
fulfils
fumigate
fumigates
functions
fungi
furling
furlong
fuzzes
gagging
gained
gallant
galloped
galore
gangrenes
gardenias
gasoline
gathered
gave
genocide
gentiles
gentler
gentlest
geology
geometric
gerbil
ghouls
gilt
gin
glacial
gladly
glamourize
glazed
glen
gloomy
glowed
glowering
glummest
glutted
gnats
gnome
goal
goblins
godly
gonna
goods
goody
gophers
gouged
governmental
grammatically
grandfather
grandfathering
graphite
grapple
grassing
grating
graving
greened
griddle
grieves
grocer
grouchiest
groupings
groups
grubbed
grubbiest
grumbled
guffaw
guidance
gunned
guppies
gurgles
guying
gyroscope
haddock
haddocks
haggled
hails
halts
handcuffed
handful
handicap
handles
hangings
hangover
harasses
harrying
harshness
haves
haziest
headquarters
headway
heartening
heat
heaves
hellish
hemorrhage
herring
hew
hick
hiding
highjacking
highland
hijacking
hijacks
hiking
hilarious
hill
hinged
hinging
hinting
hoax
hobbies
hocks
holocaust
holstering
honeyed
hooked
hoops
hooray
horribly
hostiles
hued
huffs
hulking
hullabaloos
humanized
humbles
humidify
humor
hunks
hunt
hurl
hurling
hurry
husband
husbands
hydrant
hymned
hypnotists
hypocrite
hypothesizes
hysterical
icing
icy
ideologies
idiomatic
idled
if
illuminations
images
imaginative
immediate
imminently
immobilizing
immoralities
immorality
impacted
impacts
impatiences
impeded
impediments
impenetrable
imperfection
importance
impounds
impregnable
impregnates
inadvertently
incessant
incites
incomplete
inconceivable
incorporation
incurs
indexed
indicators
indigestion
indoctrinating
inertia
infant
infectious
infest
infirmary
influence
influencing
informal
infused
infuses
ingenious
inhaler
initial
initials
initiatives
injuries
innovative
inquiring
insiders
insincerely
insistent
instancing
instils
institutionalized
insulates
insulating
insults
insuring
interesting
interface
interloper
intermingle
international
interpreters
intervenes
interventions
interweaving
intestine
intolerant
intrinsically
intruded
invalids
inventorying
invisibly
involuntary
ironically
is
italics
itchier
iterations
jabber
jabbered
jackasses
jacked
jaguar
jaguars
jangling
jauntiest
jeopardize
jests
jewel
jibed
jilted
jointed
journalist
joyfuller
joyfullest
judiciary
jugular
juicy
jumbles
jumper
junta
juror
juster
jut
jute
keg
kickback
kills
kilned
kindle
kindlier
kittens
kneecaps
knit
knob
kowtowing
laggard
lambs
landed
landowner
landslid
lane
lasers
lateralled
lathing
laundry
laurels
lavisher
lead
leafletting
leap
leapfrogs
learnt
lectern
leeches
leer
leeway
legal
legality
legally
leisure
lengthier
lenses
lesbian
levering
levied
lexicons
libeling
liberate
lifeboats
lifeguard
lift
lightening
likeliest
limb
linchpin
line
linguistics
links
liquifies
listeners
litany
lithium
liturgy
livid
loaves
lobbying
logic
longed
loonier
loophole
loosened
lords
lotions
louse
luck
lucking
lugs
lurching
lushest
machinery
maggots
magicians
magnificence
mainline
majestic
majestically
majority
making
malpractice
mangroves
mangy
manners
mantlepieces
manually
margins
marshalling
marvelled
masculines
masked
masts
mathematically
mavericks
maximized
maximizes
mealiest
meaningless
medias
medicating
melodramas
melting
memoirs
menagerie
mergers
mesdames
mesh
metropolis
midday
migraine
migrate
migratory
mild
milder
mind
minion
ministers
ministry
minnows
miscarriages
misconceptions
misconstrued
misguide
misquoting
misrepresents
mitigating
mobbed
mobbing
mod
models
modes
modified
modulating
molasses
mold
moldy
monarchs
monkeying
moos
mooting
morsels
mortuaries
mosaics
moustache
muffed
muffling
mulching
mummies
murdered
must
mysterious
mythologies
nabbed
naively
nakedness
nauseated
nauseates
necklace
necktie
neediest
negligs
negotiated
neighbored
neutron
newbies
newest
newsier
niece
niftier
nightmare
nipped
nipple
noble
nosiest
notebook
noticeable
nought
nouns
nuclei
nucleus
nullified
nurture
nutted
objectionable
objective
objectively
obliterating
obnoxious
obscener
obscenities
observer
obstruction
occasional
offender
offense
officer
offset
oil
omen
omniscient
on
one
oodles
ooze
opened
opening
operator
operators
opium
optimal
optimism
optimistic
optimize
optional
oration
orchestrating
orchids
ordains
organic
organics
organized
ornaments
orphaning
oscillate
oscillations
otter
ourselves
outburst
outcasts
outclassing
outdoor
outlaw
outlived
output
outputting
outrage
outsets
overate
overcast
overcasts
overdid
overflowed
overhead
overlaying
overreacting
overshoot
overthrowing
overtures
overwhelm
packages
paddled
paddocked
pads
paintings
paired
palace
palls
panaceas
panel
panelling
pangs
panhandlers
panhandling
parameters
parked
parliament
parsley
parsons
part
partridges
patched
patent
paternal
patienter
patio
pattering
payable
payoff
pedagogy
peddled
peering
peeve
peeving
pelvic
penniless
pensively
peopled
peppermint
perfections
perishing
perkier
perpetrated
persuade
persuading
pessimist
petrifies
pews
pharmacist
philanthropy
phobias
phonetics
photos
physicist
pickaback
pickaxing
picket
pickpocket
piddles
piggish
pikes
pimples
pinnacle
pique
pis
pitch
piteously
pithy
pixie
placed
plank
planks
planners
plants
played
pleasant
pleasantries
pleasurable
pledge
plied
plod
plot
plowed
plugging
plume
plums
poached
pocketed
pointers
polarizes
polished
polkaed
pollutes
polygons
ponderous
poops
poppy
popular
portended
portfolio
portliest
positive
possession
possessives
possessors
possibly
posterior
posts
potting
powers
preconception
preempt
prefixed
prefixes
prefixing
prehistoric
prejudicial
preludes
prepaying
prepositions
prescribing
presentation
preservation
preside
presided
presses
pretend
pretenders
pretentiously
pretexts
pretzels
prevalence
pried
principal
principalities
private
privies
profanity
prognoses
programmable
prohibitive
prologs
prolonging
promotions
properer
properly
prosecutes
prospers
protocols
provocation
provocative
prowler
psychiatry
psychopath
puddled
puffiest
pulls
pulsating
pulsations
punctuality
punished
punning
purchases
pureeing
purges
purity
purport
purporting
pursing
pursuing
pushy
pussiest
puttied
quadrangles
quadruples
quaintest
qualifications
quelling
questions
quests
queuing
quickens
quicksand
quintets
quintuplets
quips
quitted
quiver
race
raffle
ranger
ranker
rankles
rasping
ravages
ravenous
razor
readjusts
realist
realty
reappearing
recital
reckons
reclines
recognizes
recompensing
recorder
recuperated
recurred
recursive
recycles
redefines
redistributes
redressed
reduced
referenced
reformatted
refreshed
refuses
regime
region
regretting
regularity
regulars
regulating
reining
reinstatement
reliance
remaining
remaking
reminiscent
removing
rendering
renovated
reopens
repealed
repealing
repel
repression
reprimanded
reproducing
reprogramming
republic
repudiating
requisitioning
rescued
resolving
resort
resourceful
resplendent
restrictive
restructure
resulting
resurgence
reticence
retrospects
revenues
reversal
reviewing
revolts
ribbing
rice
rides
ridiculing
rim
ringleaders
riot
roaches
roadsides
robuster
roosts
rouged
roughest
rudely
ruffles
ruffs
rules
ruminating
rummer
rung
runt
saboteur
sadness
saintly
salient
sally
sanatoria
sandpaper
sandwiched
sank
sap
sardine
sauce
saucing
save
savorier
sawdust
sawn
scare
scared
scars
scatter
schoolteacher
scientist
scientists
scoot
scotchs
scramming
scrawl
screeching
screened
scrub
scruple
scuffing
sculptures
scum
scurry
section
security
seeded
seeps
selfish
seminaries
senseless
sentence
sentience
servicing
settlement
severely
sexed
shadier
shaikhs
shame
shamrocks
shapeliest
sharped
she
sheave
shiftiest
shiftless
shimmering
shiniest
shoes
shoo
shooed
shore
shored
shovelling
showed
shunt
shutdown
sideshows
signposted
silent
simpler
simulate
singe
siphoning
sipped
sirens
sites
situate
sixties
skein
sketching
skills
skimps
sky
slag
slaked
slaking
slammed
slates
sledding
sleeting
slime
slipping
slobs
sloppy
slops
slouched
slows
sluice
sluicing
smash
smirked
sneakiest
sniffles
snoop
snooping
snorkel
snowplows
snuffs
sobered
socialism
sodded
solely
soloing
someone
sorcery
soundtrack
southwest
sown
spangle
spanned
specimens
specks
spectaculars
speculated
speediest
spew
spicing
spicy
spike
splurge
spokes
sponsors
spores
sporran
sportsmanship
spotty
springy
sprinting
sprung
spurn
squad
squashes
squealed
squinter
stack
stamped
staplers
starchiest
starter
statures
steadfast
stepped
stiff
stifling
stimulating
stipulates
stockades
stodgiest
stoning
storey
stories
strands
strangulation
stratums
streaming
strew
strewing
stripper
stroke
stub
stubbornest
stumping
stumps
sturdier
subdivides
subdues
subjective
submersion
submissive
subordinating
subset
substitutes
subtractions
suburban
suckle
suctioning
sugar
suggest
suicide
suited
summer
sundaes
suntanned
super
superiority
superscript
supplanted
supplements
supporters
surgery
surges
suspiciously
swaggering
swallows
swamped
sweet
sweetheart
swerve
swiftly
swim
swine
swollen
syllable
symbols
sympathetically
sympathizing
sympathy
synagogs
synonymous
synthesizers
tablecloth
tabling
tabus
tackier
tags
tailgates
tars
tartest
tasteful
taxpayer
teetotalers
teetotaller
television
temperate
tempos
tempt
tend
tenement
tenser
tensions
tepid
terminology
terrorist
thanks
thawed
theaters
thereon
thin
thing
thinned
thinnest
thoughtfulness
thrashing
threshers
throwing
thrusting
tiaras
tick
tidal
tightly
tilted
timelier
titillated
today
toddles
toga
tolling
tombing
tombstone
tonics
tonight
tormenters
torpedoes
torrid
torsi
tossed
totalled
touchdown
towards
towelled
trading
trampled
tranquillized
transforms
transient
transmission
transmitter
trapezoid
travel
treason
treatments
trenching
trendy
trespassers
tricked
trigger
trilogies
trilogy
tripped
trolls
trounce
trowelling
trues
trusts
tubas
turmoil
turn
turnpike
turrets
turtles
tusks
twice
twiddles
twined
twines
twitched
twitches
tying
typify
tyranny
unbearable
unbelievable
unceasing
unconnected
unconstitutional
undecided
undercurrent
undergo
undernourished
underrates
understudying
unequivocal
unfurls
unhappiness
unhelpful
uniqueness
uniquer
universally
unkindest
unlabeled
unloaded
unnamed
unpacking
unpleasantness
unraveling
unsophisticated
untold
unveiling
unwound
upbeat
upbeats
update
upped
usually
usurps
utilitarian
vacancies
vaccinates
vacuuming
vaginas
vandalism
vandalizing
vastest
vats
veers
veiling
ventilates
ventilation
veriest
vest
vicars
victorious
vigilante
vigor
vile
vilify
vindicates
vineyards
viral
visioning
vivisection
vocations
volunteering
waffles
wager
wagering
wailing
waists
wakened
wallets
wallows
walls
wander
wandering
wane
wariest
warlike
warranting
washout
wastage
watchdog
watertight
watery
waviest
waxes
weaken
wearying
weaver
weaves
wedge
weed
weeding
weeing
weekdays
weeklies
weirdness
welds
welt
weltered
whether
whets
while
whipping
whirrs
whistles
whiter
whittles
windfalls
windscreen
winking
winter
winteriest
witched
wither
wobble
wobbles
wolfs
wolves
wonderland
woodies
workmanship
worse
would
wound
woven
wrangle
wrest
wrested
writable
wronging
yoking
yowl
yowling
zeal
zinced
zoom
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
""".split('%\n')

if __name__ == "__main__":
    main()

