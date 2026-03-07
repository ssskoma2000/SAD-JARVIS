import React, { Suspense, useEffect, useRef } from 'react';
import Spline, { SplineEvent } from '@splinetool/react-spline';

/**
 * Jarvis 3D modelini ko'rsatuvchi va animatsiyalarni boshqaruvchi komponent.
 * @param {{ animationTriggers: Array<object> }} props
 *   - animationTriggers: Backend'dan keladigan animatsiya obyektlari massivi.
 *     Masalan: [{ name: 'nod_head', value: 1 }, { name: 'blink', value: 0.8 }]
 */
const JarvisModel = ({ animationTriggers }) => {
    const splineRef = useRef();

    /**
     * Spline obyektini yuklaydi.
     * @param {any} spline - Spline ilovasi obyekti.
     */
    function onLoad(spline) {
        splineRef.current = spline;
        console.log("Spline sahnasi muvaffaqiyatli yuklandi.");
    }

    /**
     * Sichqoncha bosilganda ishlaydigan funksiya.
     * @param {SplineEvent} e - Spline hodisasi.
     */
    function onMouseDown(e) {
        // Agar "JarvisHead" nomli obyekt bosilsa, "click_reaction" event'ini ishga tushirish
        if (e.target.name === 'JarvisHead') {
            console.log("Jarvis boshi bosildi!");
            splineRef.current?.emitEvent('mouseDown', 'click_reaction');
        }
    }

    /**
     * Sichqoncha obyekt ustiga kelganda ishlaydigan funksiya.
     * @param {SplineEvent} e - Spline hodisasi.
     */
    function onMouseEnter(e) {
        // Agar sichqoncha "JarvisHead" ustiga kelsa, "hover_effect" event'ini ishga tushirish
        if (e.target.name === 'JarvisHead') {
            console.log("Sichqoncha Jarvis boshi ustida!");
            splineRef.current?.emitEvent('mouseHover', 'hover_effect');
        }
    }

    useEffect(() => {
        const spline = splineRef.current;
        if (spline && animationTriggers && animationTriggers.length > 0) {
            console.log("Animatsiya triggerlari qabul qilindi:", animationTriggers);

            // Har bir trigger uchun Spline'dagi tegishli Event'ni ishga tushirish
            animationTriggers.forEach(trigger => {
                // `trigger.name` bu Spline'dagi Event (yoki State) nomi bo'lishi kerak.
                // Masalan: "nod_head", "confirm_action", "coding_effect"
                console.log(`'${trigger.name}' nomli Spline Event'i ishga tushirilmoqda.`);
                spline.emitEvent('start', trigger.name); // 'start' hodisasi orqali eventni ishga tushirish
            });
        }
    }, [animationTriggers]);

    return (
        <div className="absolute inset-0 z-0">
            <Suspense fallback={<div className="w-full h-full flex items-center justify-center text-white">Yuklanmoqda...</div>}>
                <Spline
                    scene="https://prod.spline.design/m3L2a4YJj9tZ-kYn/scene.splinecode" // BU YERGA O'ZINGIZNING SPLINE SAHNANGIZ URL'INI QO'YING
                    onLoad={onLoad}
                    onMouseDown={onMouseDown}
                    onMouseEnter={onMouseEnter}
                />
            </Suspense>
        </div>
    );
};

export default JarvisModel;