import createCache from '@emotion/cache';

const isBrowser = typeof document !== 'undefined';

// Emotionのキャッシュ作成関数（SSRとクライアント側でスタイルが一致するようにキーを設定）
export default function createEmotionCache() {
  let insertionPoint: HTMLElement | undefined;

  if (isBrowser) {
    const emotionInsertionPoint = document.querySelector<HTMLMetaElement>(
      'meta[name="emotion-insertion-point"]',
    );
    insertionPoint = emotionInsertionPoint ?? undefined;
  }

  return createCache({ key: 'mui-style', insertionPoint });
}
