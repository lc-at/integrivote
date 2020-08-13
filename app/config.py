MASTER_PASSWORD = 'password'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///votes.db'
SECRET_KEY = 'jfnurjsefhnciukjdshfnieckj,rhn43ikn'

APP_NAME = 'Smanika Klik Serentak'
ELECTION_EVENT_NAME = ' '.join(('Pemilihan Ketua dan Wakil Ketua OSIS',
                                'SMA Negeri 1 Sumbawa Besar', '2020/2021'))
ELECTION_EVENT_HOST = 'OSIS SMA Negeri 1 Sumbawa Besar'
COPYRIGHT_YEAR = 2020

STUDENTS_CSV = 'data_siswa.csv'

CANDIDATES = [
    '(1) Muhammad Fajrin Ramadhani, Adinda Olgha JP',
    '(2) Arkam Haryadi, Dina Rahidatul Adiat',
    '(3) Septian Eka Rahmadi, Marsya Salsabila'
]

CLASSES = ['10', '11', '12']

PREFERENCES_FIELDS = {
    'MASTER_PASSWORD': (str, '5f4dcc3b5aa765d61d8327deb882cf99'),
    'ACCEPTS_VOTE': (int, 1)
}
