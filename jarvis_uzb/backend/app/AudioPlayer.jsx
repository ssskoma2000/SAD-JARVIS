import { useEffect, useRef } from 'react';

/**
 * Base64 formatdagi audioni avtomatik ijro etuvchi komponent.
 * @param {{ audioBase64: string }} props
 */
const AudioPlayer = ({ audioBase64 }) => {
    const audioRef = useRef(null);

    useEffect(() => {
        if (audioBase64) {
            // Base64 ma'lumotidan audio manbasini yaratish.
            // Backend mp3 formatida yuborgani uchun 'audio/mp3' ishlatamiz.
            const audioSrc = `data:audio/mp3;base64,${audioBase64}`;

            if (!audioRef.current) {
                audioRef.current = new Audio(audioSrc);
            } else {
                audioRef.current.src = audioSrc;
            }

            // Audioni ijro etish
            audioRef.current.play().catch(error => {
                console.error("Audio ijro etishda xatolik:", error);
                // Brauzerlar foydalanuvchi sahifa bilan o'zaro aloqada bo'lmaguncha avtomatik ijro etishni bloklashi mumkin.
            });
        }
    }, [audioBase64]);

    return null; // Bu komponentning ko'rinadigan UI qismi yo'q.
};

export default AudioPlayer;