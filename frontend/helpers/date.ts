export const dateApiFormat = new Intl.DateTimeFormat('en-CA', {});

export const getDateWithoutZone = (dateStr: string) => new Date(dateStr.split('+')[0]);

export const dateHumanShortFormat = new Intl.DateTimeFormat('ru', {
    day: '2-digit', month: 'short'
});

export const dateHumanYearFormat = new Intl.DateTimeFormat('ru', {
    day: '2-digit', month: 'short', year: 'numeric'
});

export const dateHumanFullFormat = new Intl.DateTimeFormat('ru', {
    dateStyle: 'medium', timeStyle: 'medium'
});

export const formatMinutesToHHMM = (value: number|string) => {
    const total = typeof value === 'string' ? Number(value) : value;
    const minutes = total % 60;
    const hours = (total - minutes) / 60;

    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
};

export const currentYear = new Date().getFullYear();
