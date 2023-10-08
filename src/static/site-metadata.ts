interface ISiteMetadataResult {
  siteTitle: string;
  siteUrl: string;
  description: string;
  keywords: string;
  logo: string;
  navLinks: {
    name: string;
    url: string;
  }[];
}

const data: ISiteMetadataResult = {
  siteTitle: 'Workouts Map',
  siteUrl: 'http://yuzhuohui.info/workouts_page/',
  logo: 'https://avatars.githubusercontent.com/u/413855?v=4',
  description: 'Personal site and blog',
  keywords: 'workouts, running, cycling, riding, roadtrip, hiking, swimming',
  navLinks: [
    {
      name: 'Blog',
      url: 'https://www.yuzhuohui.info',
    },
    {
      name: 'About',
      url: 'https://github.com/agassiyzh/workouts_page/blob/master/README-CN.md',
    },
  ],
};

export default data;
