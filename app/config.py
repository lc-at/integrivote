MASTER_PASSWORD = 'password'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///votes.db'
SECRET_KEY = 'jfnurjsefhnciukjdshfnieckj,rhn43ikn'

ELECTION_EVENT_NAME = ' '.join(('Pemilihan Ketua dan Wakil Ketua OSIS',
                                'SMA Negeri 1 Sumbawa Besar', '2020/2021'))
ELECTION_EVENT_HOST = 'OSIS SMA Negeri 1 Sumbawa Besar'
COPYRIGHT_YEAR = 2020

CANDIDATES = [
    '(1) Muhammad Fajrin Ramadhani, Adinda Olgha JP',
    '(2) Arkam Haryadi, Dina Rahidatul Adiat',
    '(3) Septian Eka Rahmadi, Marsya Salsabila'
]
CLASSES = [
    'X MIA 1',
    'X MIA 2',
    'X MIA 3',
    'X MIA 4',
    'X MIA 5',
    'X IIS 1',
    'X IIS 2',
    'X IIS 3',
    'XI MIA 1',
    'XI MIA 2',
    'XI MIA 3',
    'XI MIA 4',
    'XI MIA 5',
    'XI MIA 6',
    'XI IIS 1',
    'XI IIS 2',
    'XI IIS 3',
    'XI MIA 1',
    'XII MIA 2',
    'XII MIA 3',
    'XII MIA 4',
    'XII MIA 5',
    'XII IIS 1',
    'XII IIS 2',
    'XII IIS 3',
]

PREFERENCES_FIELDS = {
    'MASTER_PASSWORD': (str, '5f4dcc3b5aa765d61d8327deb882cf99'),
    'ACCEPTS_VOTE': (int, 1)
}
